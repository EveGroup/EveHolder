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
from .models import Visitor, Event, Host, Notification, NotificationUser


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


@unauthenticated_user
def register_page(request):
    """Register account for both visitor_registered_events and host.

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
            phone_num = request.POST.get('phone_number')
            group_name = request.POST.get('type')

            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            login(request, user)

            if group_name == 'Visitor':
                Visitor.objects.create(user=user, name=username, email=email, phone_num=phone_num)
                return redirect('eve_holder:visitor_registered_events')
            elif group_name == 'Host':
                Host.objects.create(user=user, name=username, email=email)
                return redirect('eve_holder:host')

    context = {'form': form}

    return render(request, 'eve_holder/accounts/register.html', context)


# about login logout and register
@unauthenticated_user
def login_page(request):
    """Login for both visitor_registered_events and host.

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
            login(request, user)
            group = request.user.groups.all()[0].name
            print(group)
            if group == 'Host':
                return redirect('eve_holder:host')
            elif group == 'Visitor':
                return redirect('eve_holder:visitor_registered_events')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}

    return render(request, 'eve_holder/accounts/login.html', context)


def logout_page(request):
    """Logged out for both visitor_registered_events and host.

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
    events_list = request.user.host.event_set.all().order_by('-pub_date')
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'host': get_host, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/hosts/host.html', context)


# for host
@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitor'])
def visitor_registered_events(request):
    """Visitor dashboard.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the visitor page with the context.
    """
    visitor_id = request.user.visitor.id
    get_visitor = Visitor.objects.get(id=visitor_id)
    events_list = get_visitor.event.all().order_by('-pub_date')
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'visitor_registered_events': get_visitor, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter,
               }

    return render(request, 'eve_holder/visitors/visitor_registered_events.html', context)


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

    return render(request, 'eve_holder/visitors/visitor_info.html', {'visitor': visitor})


@login_required(login_url='eve_holder:login')
@host_only
def visitors_list(request, pk):
    """All visitor that register in that event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk: visitor's id.

    Returns:
        render: Render the visitor_registered_events list page with the context.
    """
    event = Event.objects.get(id=pk)
    list_visitors = Visitor.objects.filter(event=event).order_by('name')
    visitors_count = list_visitors.count()
    context = {'event': event, 'visitor_registered_events': list_visitors, 'visitors_count':visitors_count}
    return render(request, 'eve_holder/visitors/visitors_list.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitor'])
def events(request):
    """All events in the application.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render the events page with events list.
    """
    visitor_id = request.user.visitor.id
    visitor = Visitor.objects.get(id=visitor_id)
    registered_events_list = visitor.event.all().order_by('-pub_date')
    events_list = Event.objects.exclude(pk__in=registered_events_list)
    return render(request, 'eve_holder/events/events.html', {'events': events_list})


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
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            event = Event.objects.get(event_name=form.cleaned_data.get('event_name'))

            if not event.check_pub_date():
                messages.info(request, "End date cannot come before publish date.")
            elif not event.check_event_date():
                messages.info(request, "Event date cannot come before publish date.")
            else:
                # for person in get_host:
                form.save()
                event.event_host.add(get_host)
                return redirect('eve_holder:host')

    btn = "Create"
    context = {'form': form, 'host': request.user, 'btn': btn}

    return render(request, 'eve_holder/hosts/create_event.html', context)


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
    visitors_list = Visitor.objects.filter(event=events_list)
    form = EventForm(instance=events_list)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=events_list)
        if form.is_valid():
            create_notification(events_list, visitors_list, 'info')
            form.save()
            return redirect('eve_holder:host')

    btn = "Edit"
    context = {'form': form, 'btn':btn}

    return render(request, 'eve_holder/hosts/create_event.html', context)


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
    visitors_list = Visitor.objects.filter(event=events_list)
    if request.user.groups.all()[0].name == 'Host':
        create_notification(events_list, visitors_list, 'warning')
        events_list.delete()
    return redirect('eve_holder:host')


@login_required(login_url='eve_holder:login')
@allowed_users(['Host', 'Visitor'])
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
    if user.groups.filter(name='Visitor').exists():
        visitor = request.user.visitor
        context = {'event': event, 'host_name': get_first_host_name, 'visitor': visitor}
        return render(request, 'eve_holder/events/event_detail.html', context)
    elif user.groups.filter(name='Host').exists():
        context = {'event': event, 'host_name': get_first_host_name}
        return render(request, 'eve_holder/hosts/host_event_detail.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitor'])
def event_register(request, pk_event):
    """For visitor register event.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk_event: event's id

    Returns:
        render: Render the event_registration page with the context.
    """
    visitor = Visitor.objects.get(user=request.user)
    form = EventRegistrationForm(instance=visitor)
    event = Event.objects.get(id=pk_event)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=visitor)
        if form.is_valid():
            visitor.event.add(event)
            form.save()
            return redirect('eve_holder:visitor_registered_events')

    context = {'form': form, 'event': event}
    return render(request, 'eve_holder/join_event.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Visitor'])
def cancel_event(request, pk_event):
    """For cancel the event use with visitor's accounts.

    Args:
        request: A HttpRequest object, which contains data about the request.
        pk_event: event's id.

    Returns:
        render: Render the cancel event page with the context.

    """
    visitor = Visitor.objects.get(user=request.user)
    my_event = Event.objects.get(id=pk_event)
    if request.method == 'POST':
        visitor.event.remove(my_event)
        return redirect('eve_holder:visitor_registered_events')
    events_list = Event.objects.get(id=pk_event)
    context = {'item': events_list}
    return render(request, 'eve_holder/events/event_cancel.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Visitor'])
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
        return redirect('eve_holder:visitor_registered_events')
    context = {'user_form': user_form, 'visitor_form': visitor_form}
    return render(request, 'eve_holder/visitors/visitor_update_information.html', context)


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
        return redirect('eve_holder:host')
    context = {'user_form': user_form, 'host_form': host_form}
    return render(request, 'eve_holder/hosts/host_update_information.html', context)


@login_required(login_url='login')
@allowed_users(['Host', 'Visitor'])
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
    if request.method == 'POST':
        user = User.objects.get(id=user.id)
        if user.groups.filter(name='Host').exists():
            host = Host.objects.get(user=user)
            host_events = host.event_set.all()
            host_events.delete()
        user.delete()
        return redirect('eve_holder:homepage')
    return render(request, 'eve_holder/delete_account.html', context)


@login_required(login_url='login')
@allowed_users(['Host', 'Visitor'])
def my_account(request):
    user = request.user
    if user.groups.filter(name='Visitor').exists():
        visitor_id = request.user.visitor.id
        get_visitor = Visitor.objects.get(id=visitor_id)
        events_list = get_visitor.event.all()
        events_count = events_list.count()
        notify = Notification.objects.filter(visitor=get_visitor).order_by('-created')
        context = {
            'visitor_registered_events': get_visitor,
            'events_count': events_count,
            'notifications': notify,
        }
        return render(request, 'eve_holder/visitors/visitor_my_account.html', context)
    elif user.groups.filter(name='Host').exists():
        host_id = user.host.id
        get_host = Host.objects.get(id=host_id)
        events_list = request.user.host.event_set.all()
        events_count = events_list.count()
        context = {'host': get_host, 'events': events_list,
                   'events_count': events_count}
        return render(request, 'eve_holder/hosts/host_my_account.html', context)


@login_required(login_url='login')
@allowed_users(['Host', 'Visitor'])
def search_event(request):
    """Search for particular event.

    Args:
        request: A HttpRequest object, which contains data about the request.

    Returns:
        render: Render page of results found.
        redirect: Redirect to homepage.
    """
    requested_events = request.POST['search']
    previous_page = request.META['HTTP_REFERER']
    if requested_events != "":
        filtered_events = Event.objects.filter(event_name__contains=requested_events)
        if not filtered_events.exists():
            messages.warning(request, "No result found for \"" + requested_events + "\"")
        context = {'events': filtered_events, 'requested_events': requested_events}
        return render(request, 'eve_holder/search_event.html', context)
    messages.warning(request, "Search field is Empty.")
    return redirect(previous_page)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Visitor'])
def close_notification(request, pk):
    """Close the specified notification for the user, if that notification is
    the last one delete the notification object.

    Arguments:
        pk: the primary keys of the notification objects

    Returns:
        redirect: Redirected to my_account
    """
    notification = Notification.objects.get(id=pk)
    visitor = Visitor.objects.get(user=request.user)
    notify = NotificationUser.objects.get(notification=notification, visitor=visitor)
    notify.delete()
    notification.visitor.remove(visitor)
    if not Visitor.objects.filter(notification=notification).exists():
        notification.delete()
    return redirect('eve_holder:my_account')

def create_notification(event: Event, visitors_list, level: str):
    """Find the specified notification from the event if found delete it.
    
    Arguments:
        event: Event object to filter the notification
        visitors_list: Visitor objects as queryset to add in notification
        level: "info" - for edited event, "warning" - for deleted event

    Exceptions:
        ValueError: raise when get unknown level of notification as arguments
    
    """
    if Notification.objects.filter(event=event).exists():
        notify = Notification.objects.get(level='info', event=event)
        notify.delete()

    if level == 'info':
        notify = Notification.objects.create(text=f"Event Edited: {event}", level='info', event=event)
    elif level == 'warning':
        notify = Notification.objects.create(text=f"Event Deleted: {event}", level='warning')
    else:
        raise ValueError("Unknown level of notifications")

    for person in visitors_list:
        notify.visitor.add(person)
    notify.save()
