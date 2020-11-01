"""This module contains views of the website."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .filters import EventFilter
from .forms import EventForm, CreateUserForm, EventRegistrationForm
# Create your views here.
from .models import Visitor, Event


def homepage(request):
    event_list = Event.objects.all()
    context = {'events': event_list}

    return render(request, 'eve_holder/homepage.html', context)


def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'eve_holder/event_detail.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('eve_holder:dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('eve_holder:login')
        context = {'form': form}

        return render(request, 'eve_holder/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('eve_holder:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('eve_holder:dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}

        return render(request, 'eve_holder/login.html', context)


def logout_page(request):
    logout(request)

    return redirect('eve_holder:login')


@login_required(login_url='eve_holder:login')
def dashboard(request):
    visitors_list = Visitor.objects.all()
    events_list = Event.objects.all()

    total_events = events_list.count()

    context = {'visitors': visitors_list, 'events': events_list, 'total_events': total_events}

    return render(request, 'eve_holder/dashboard.html', context)


@login_required(login_url='eve_holder:login')
def events(request):
    events_list = Event.objects.all()

    return render(request, 'eve_holder/events.html', {'events': events_list})


@login_required(login_url='eve_holder:login')
def visitors_list(request, pk):
    event = Event.objects.get(id=pk)
    visitors = Visitor.objects.filter(visitor_event=event)
    context = {'event': event, 'visitors': visitors}
    return render(request, 'eve_holder/visitors_list.html', context)


@login_required(login_url='eve_holder:login')
def visitors(request, pk):
    visitors_list = Visitor.objects.get(id=pk)
    events_list = visitors_list.visitor_event.all()
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'visitors': visitors_list, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/visitor.html', context)


@login_required(login_url='eve_holder:login')
def visitor_information(request, pk):
    visitor = Visitor.objects.get(id=pk)

    return render(request, 'eve_holder/visitor_info.html', {'visitor': visitor})


@login_required(login_url='eve_holder:login')
def create_event(request, pk):
    visitors_list = Visitor.objects.get(id=pk)
    form = EventForm(initial={'visitor': visitors_list})
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eve_holder:dashboard')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='eve_holder:login')
def edit_event(request, pk):
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
def delete_event(request, pk):
    events_list = Event.objects.get(id=pk)
    if request.method == 'POST':
        events_list.delete()
        return redirect('eve_holder:dashboard')

    context = {'item': events_list}

    return render(request, 'eve_holder/delete.html', context)


@login_required(login_url='eve_holder:login')
def event_register(request, pk):
    visitor = Visitor.objects.get(id=request.user.id)
    form = EventRegistrationForm(instance=visitor)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('eve_holder:dashboard')
    context = {'form': form}
    return render(request, 'eve_holder/event_registration.html', context)

