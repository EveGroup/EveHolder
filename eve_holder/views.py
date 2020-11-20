"""This module contains views of the website."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from .decorations import unauthenticated_user, allowed_users, host_only
from .filters import EventFilter
from .forms import EventForm, CreateUserForm, EventRegistrationForm, UpdateInformationUserForm, \
    UpdateInformationVisitorForm, UpdateInformationHostForm
from .models import Visitor, Event, Host


# Any one can view this below page.
def homepage(request):
    """Home page of the application.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the homepage with the context.
    """
    event_list = Event.objects.all()
    context = {'events': event_list}

    return render(request, 'eve_holder/homepage.html', context)


def dashboard(request):
    """Main dashboard.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the dashboard page with the context.
    """
    get_visitors = Visitor.objects.all()
    get_events = Event.objects.all()

    total_events = get_events.count()

    context = {'visitors': get_visitors, 'events': get_events, 'total_events': total_events}

    return render(request, 'eve_holder/dashboard.html', context)


@unauthenticated_user
def register_page(request):
    """Register account for both visitors and host.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the register page with the context.
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group_name = form.cleaned_data.get('groups')[0]

            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            # add user to Host or Visitor
            if group_name == Group.objects.get(name='Visitors'):
                Visitor.objects.create(user=user, name=username, email=email)
            elif group_name == Group.objects.get(name='Host'):
                Host.objects.create(user=user, name=username, email=email)

            messages.success(request, 'Account was created for ' + username)
            return redirect('eve_holder:login')
    context = {'form': form}

    return render(request, 'eve_holder/re.html', context)


# about login logout and register
@unauthenticated_user
def login_page(request):
    """Login for both visitors and host.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the login page with the context.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if user.groups.filter(name='Visitors').exists():
            #     return redirect('eve_holder:visitors')
            login(request, user)
            # print
            group = request.user.groups.all()[0].name
            if group == 'Host':
                return redirect('eve_holder:host')
            elif group == 'Visitors':
                return redirect('eve_holder:visitor')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}

    return render(request, 'eve_holder/login.html', context)


def logout_page(request):
    """Logged out for both visitors and host.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the logout page with the context.
    """
    logout(request)

    return redirect('eve_holder:homepage')


@login_required(login_url='eve_holder:login')
@host_only
def host(request):
    """Host dashboard.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the host page with the context.
    """
    host_id = request.user.host.id
    get_host = Host.objects.get(id=host_id)
    events_list = request.user.host.event_set.all()
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'host': get_host, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/host.html', context)


# for host
@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def visitors(request):
    """Visitor dashboard.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the visitor page with the context.
    """
    visitor_id = request.user.visitor.id
    get_visitors = Visitor.objects.get(id=visitor_id)
    events_list = get_visitors.event.all()
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'visitors': get_visitors, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/visitor.html', context)


@login_required(login_url='eve_holder:login')
@host_only
def visitor_information(request, pk):
    """Host view visitor that register event information.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: visitor's id.

    Returns:
        render: Render the visitor information page with the context.
    """
    visitor = Visitor.objects.get(id=pk)

    return render(request, 'eve_holder/visitor_info.html', {'visitor': visitor})


@login_required(login_url='eve_holder:login')
@host_only
def visitors_list(request, pk):
    """All visitor that register in that event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: visitor's id.

    Returns:
        render: Render the visitors list page with the context.
    """
    event = Event.objects.get(id=pk)
    list_visitors = Visitor.objects.filter(event=event)
    context = {'event': event, 'visitors': list_visitors}
    return render(request, 'eve_holder/visitors_list.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def events(request):
    """All events in the application.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the events page with events list.
    """
    visitor_id = request.user.visitor.id
    visitor = Visitor.objects.get(id=visitor_id)
    registered_events_list = visitor.event.all()
    events_list = Event.objects.exclude(pk__in=registered_events_list)
    # return render(request, 'eve_holder/events.html', {'events': events_list, 'visitor_events':
    # registered_events_list})
    return render(request, 'eve_holder/events.html', {'events': events_list})


@login_required(login_url='eve_holder:login')
@host_only
def create_event(request):
    """Host create event.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the create event page with the context.
    """
    host_id = request.user.host.id
    get_host = Host.objects.get(id=host_id)
    form = EventForm(initial={'event_host': get_host})
    if request.method == 'POST':
        form = EventForm(request.POST)
        # form.event_host = request.user
        # form['event_host'] = request.user
        # print(form)
        if form.is_valid():
            # form.event_host = request.user
            # print(form.event_host)
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('eve_holder:host')

    context = {'form': form, 'host': request.user}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='eve_holder:login')
@host_only
def edit_event(request, pk):
    """Host edit event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: event's id.

    Returns:
        render: Render the edit event page with the context.
    """
    events_list = Event.objects.get(id=pk)
    form = EventForm(instance=events_list)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=events_list)
        if form.is_valid():
            messages.info(request, f"Event Edited ({events_list})")
            form.save()
            return redirect('eve_holder:host')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='eve_holder:login')
@host_only
def delete_event(request, pk):
    """For host delete event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: event's id

    Returns:
        render: Render the delete event page with the context.
    """
    events_list = Event.objects.get(id=pk)
    if request.method == 'POST':
        events_list.delete()
        if request.user.groups.all()[0].name == 'Host':
            messages.success(request, "Event Delete Successfully")
            return redirect('eve_holder:host')

    context = {'item': events_list}

    return render(request, 'eve_holder/delete.html', context)


@login_required(login_url='eve_holder:login')
def event_detail(request, pk):
    """Detail for each event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: event's id.

    Returns:
        render: Render the event detail page with the context.
    """
    event = Event.objects.get(id=pk)
    get_first_host_name = event.event_host.values_list('name', flat=True)[0]
    user = request.user
    if user.groups.filter(name='Visitors').exists():
        visitor = request.user.visitor
        context = {'event': event, 'host_name': get_first_host_name, 'visitor': visitor}
        return render(request, 'eve_holder/event_detail.html', context)
    elif user.groups.filter(name='Host').exists():
        context = {'event': event, 'host_name': get_first_host_name}
        return render(request, 'eve_holder/host_event_detail.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def event_register(request, pk_event):
    """For visitor register event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk_event: event's id

    Returns:
        render: Render the event_registration page with the context.
    """
    # visitor = Visitor.objects.get(id=request.user.visitor.id)
    visitor = Visitor.objects.get(user=request.user)
    form = EventRegistrationForm(instance=visitor)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=visitor)
        if form.is_valid():
            event = Event.objects.get(id=pk_event)
            visitor.event.add(event)
            form.save()
            messages.success(request, "You have registered the event")
            return redirect('eve_holder:visitor')
    context = {'form': form}
    return render(request, 'eve_holder/event_registration.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Visitors'])
def cancel_event(request, pk_event):
    """For cancel the event use with visitor's accounts.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk_event: event's id.

    Returns:
        render: Render the cancel event page with the context.

    """
    # visitor = Visitor.objects.get(id=request.user.visitor.id)
    visitor = Visitor.objects.get(user=request.user)
    my_event = Event.objects.get(id=pk_event)
    if request.method == 'POST':
        # print("events bef", visitor.event)
        visitor.event.remove(my_event)
        messages.success(request, "Event Cancel Successfully")
        return redirect('eve_holder:visitor')
    events_list = Event.objects.get(id=pk_event)
    context = {'item': events_list}
    return render(request, 'eve_holder/event_cancel.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Visitors'])
def visitor_update_information(request):
    """Update the visitor's information.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the update information page with the context.

    """
    user = request.user
    visitor = Visitor.objects.get(user=user)
    visitor_form = UpdateInformationVisitorForm(instance=visitor)
    user_form = UpdateInformationUserForm(instance=user)
    if request.method == 'POST':
        user_form = UpdateInformationUserForm(request.POST, instance=user)
        user_form.save()
        visitor_form = UpdateInformationVisitorForm(request.POST, instance=visitor)
        visitor_form.save()
        messages.success(request, "Account Updated")
        return redirect('eve_holder:visitor')
    context = {'user_form': user_form, 'visitor_form': visitor_form}
    return render(request, 'eve_holder/visitor_update_information.html', context)


@login_required(login_url='login')
@host_only
def host_update_information(request):
    """Update the host's information.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the update information page with the context.

    """
    user = request.user
    get_first_host_name = Host.objects.get(user=user)
    host_form = UpdateInformationHostForm(instance=get_first_host_name)
    user_form = UpdateInformationUserForm(instance=user)
    if request.method == 'POST':
        user_form = UpdateInformationUserForm(request.POST, instance=user)
        user_form.save()
        host_form = UpdateInformationHostForm(request.POST, instance=get_first_host_name)
        host_form.save()
        messages.success(request, "Account Updated")
        return redirect('eve_holder:host')
    context = {'user_form': user_form, 'host_form': host_form}
    return render(request, 'eve_holder/host_update_information.html', context)


@login_required(login_url='login')
def delete_account(request):
    """Delete requested account.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        redirect: Redirect to homepage.
        render: A render page for delete confirmation.
    """
    user = request.user
    previous_page = request.META['HTTP_REFERER']
    context = {'previous_page': previous_page}
    # if user.groups.filter(name='visitors').exists():
    #     visitor = Visitor.objects.get(user=user)
    #     context = {'visitor': visitor}
    # elif user.groups.filter(name='host').exists():
    #     host = Host.objects.get(user=user)
    #     context = {'host': host}
    if request.method == 'POST':
        user = User.objects.get(id=user.id)
        messages.success(request, f"Account Deleted ({user.username})")
        user.delete()
        return redirect('eve_holder:dashboard')
    return render(request, 'eve_holder/delete_account.html', context)


@login_required(login_url='login')
def my_account(request):
    user = request.user
    if user.groups.filter(name='Visitors').exists():
        visitor_id = request.user.visitor.id
        get_visitors = Visitor.objects.get(id=visitor_id)
        events_list = get_visitors.event.all()
        events_count = events_list.count()
        context = {'visitors': get_visitors, 'events_count': events_count}
        return render(request, 'eve_holder/visitor_my_account.html', context)
    elif user.groups.filter(name='Host').exists():
        host_id = user.host.id
        get_host = Host.objects.get(id=host_id)
        events_list = request.user.host.event_set.all()
        events_count = events_list.count()
        context = {'host': get_host, 'events': events_list,
                   'events_count': events_count}
        return render(request, 'eve_holder/host_my_account.html', context)


def search_event(request):
    """Search for particular event.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render page of results found.
        redirect: Redirect to homepage.
    """
    requested_events = request.POST['search']
    if requested_events != "":
        filtered_events = Event.objects.filter(event_name__contains=requested_events)
        # print(filtered_events)
        # if filtered_events.exists():
        if not filtered_events.exists():
            messages.warning(request, "No result found for \"" + requested_events + "\"")
        context = {'events': filtered_events, 'requested_events': requested_events}
        return render(request, 'eve_holder/search_event.html', context)
    messages.warning(request, "Search field is Empty.")
    return redirect('eve_holder:dashboard')
