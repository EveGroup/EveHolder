"""This module contains views of the website."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .filters import EventFilter
from .forms import EventForm, CreateUserForm, EventRegistrationForm
from .models import Visitor, Event, Host
from .decorations import unauthenticated_user, allowed_users, host_only


# Any one can view this below page.
def homepage(request):
    """Home page of the application."""
    event_list = Event.objects.all()
    context = {'events': event_list}

    return render(request, 'eve_holder/homepage.html', context)


def event_detail(request, pk):
    """Detail for each event."""
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'eve_holder/event_detail.html', context)

@unauthenticated_user
def dashboard(request):
    """Main dashboard."""
    visitors = Visitor.objects.all()
    events_list = Event.objects.all()

    total_events = events_list.count()

    context = {'visitors': visitors, 'events': events_list, 'total_events': total_events}

    return render(request, 'eve_holder/dashboard.html', context)


# about login logout and register
@unauthenticated_user
def register_page(request):
    """Register account for both visitors and host."""
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

            print(type(group_name))
            if group_name == Group.objects.get(name='Visitors'):
                print('in vis')
                Visitor.objects.create(user=user, name=username, email=email)
            elif group_name == Group.objects.get(name='Host'):
                print('in ho')
                Host.objects.create(user=user, name=username, email=email)

            messages.success(request, 'Account was created for ' + username)
            return redirect('eve_holder:login')
    context = {'form': form}

    return render(request, 'eve_holder/register.html', context)

@unauthenticated_user
def login_page(request):
    """Login for both visitors and host."""
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
                return redirect('eve_holder:visitors')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}

    return render(request, 'eve_holder/login.html', context)


def logout_page(request):
    """Logged out for both visitors and host."""
    logout(request)

    return redirect('eve_holder:homepage')


# for host
@login_required(login_url='eve_holder:login')
@host_only
# @allowed_users(allowed_roles=['Host'])
def host(request):
    """Host dashboard."""
    # visitors_list = Visitor.objects.get(id=pk)   #  visitor list
    # host = request.user.host
    id = request.user.host.id
    host = Host.objects.get(id=id)
    events_list = request.user.host.event_set.all()
    # events_list = Event.objects.filter(event_host=host)
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'host': host, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/host.html', context)


@login_required(login_url='eve_holder:login')
@host_only
def visitors_list(request, pk):
    """Host view list of visitors."""
    event = Event.objects.get(id=pk)
    visitors_list = Visitor.objects.filter(visitor_event=event)
    context = {'event': event, 'visitors': visitors_list}
    return render(request, 'eve_holder/visitors_list.html', context)


@login_required(login_url='eve_holder:login')
@host_only
def visitor_information(request, pk):
    """Host view visitor that register event information."""
    visitor = Visitor.objects.get(id=pk)

    return render(request, 'eve_holder/visitor_info.html', {'visitor': visitor})


@login_required(login_url='eve_holder:login')
@host_only
# @allowed_users(allowed_roles=['Host'])
def create_event(request):
    """Host create event."""
    id = request.user.host.id
    host = Host.objects.get(id=id)
    form = EventForm(initial={'event_host': host})
    if request.method == 'POST':
        print('post')
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            Event.objects.create(form)
            return redirect('eve_holder:host')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='eve_holder:login')
@host_only
# @allowed_users(allowed_roles=['Host'])
def edit_event(request, pk):
    """Host edit event."""
    events_list = Event.objects.get(id=pk)
    form = EventForm(instance=events_list)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=events_list)
        if form.is_valid():
            form.save()
            return redirect('eve_holder:dashboard')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='eve_holder:login')
@host_only
# @allowed_users(allowed_roles=['Host'])
def delete_event(request, pk):
    """For host delete event."""
    events_list = Event.objects.get(id=pk)
    if request.method == 'POST':
        events_list.delete()
        return redirect('eve_holder:dashboard')

    context = {'item': events_list}

    return render(request, 'eve_holder/delete.html', context)


# for visitor
@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def visitors(request):
    """Visitor dashboard."""
    # visitor = Visitor.objects.get(id=pk)
    # events_list = visitor.event.all()
    id = request.user.visitor.id
    visitors = Visitor.objects.get(id=id)
    events_list = visitors.event.all()
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'visitors': visitors, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/visitor.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def event_register(request, pk):
    """For visitor register event. ploy"""
    visitor = Visitor.objects.get(id=request.user.visitor.id)
    form = EventRegistrationForm(instance=visitor)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('eve_holder:dashboard')
    context = {'form': form}
    return render(request, 'eve_holder/event_registration.html', context)


@login_required(login_url='eve_holder:login')
@allowed_users(allowed_roles=['Visitors'])
def events(request):
    """All events in the application."""
    events_list = Event.objects.all()

    return render(request, 'eve_holder/events.html', {'events': events_list})