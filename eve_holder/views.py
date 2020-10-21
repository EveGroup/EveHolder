"""This module contains views of the website."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .filters import EventFilter
from .forms import EventForm, CreateUserForm
# Create your views here.
from .models import Visitor, Event


def homepage(request):
    event_list = Event.objects.all()
    context = {'events': event_list}

    return render(request, 'eve_holder/homepage.html', context)


def event_detail(request):
    return render(request, 'eve_holder/event_detail.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form': form}

        return render(request, 'eve_holder/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}

        return render(request, 'eve_holder/login.html', context)


def logout_page(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    visitors_list = Visitor.objects.all()
    events_list = Event.objects.all()

    total_events = events_list.count()

    context = {'visitors': visitors_list, 'events': events_list, 'total_events': total_events}

    return render(request, 'eve_holder/dashboard.html', context)


@login_required(login_url='login')
def events(request):
    events_list = Event.objects.all()

    return render(request, 'eve_holder/events.html', {'events': events_list})


@login_required(login_url='login')
def visitors(request, pk):
    visitors_list = Visitor.objects.get(id=pk)
    events_list = visitors_list.event_set.all()
    events_count = events_list.count()

    my_filter = EventFilter(request.GET, queryset=events_list)
    events_list = my_filter.qs

    context = {'visitors': visitors_list, 'events': events_list,
               'events_count': events_count, 'my_filter': my_filter
               }

    return render(request, 'eve_holder/visitor.html', context)


@login_required(login_url='login')
def create_event(request, pk):
    visitors_list = Visitor.objects.get(id=pk)
    form = EventForm(initial={'visitor': visitors_list})
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='login')
def edit_event(request, pk):
    events_list = Event.objects.get(id=pk)
    form = EventForm(instance=events_list)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=events_list)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'eve_holder/event_form.html', context)


@login_required(login_url='login')
def delete_event(request, pk):
    events_list = Event.objects.get(id=pk)
    if request.method == 'POST':
        events_list.delete()
        return redirect('dashboard')

    context = {'item': events_list}

    return render(request, 'eve_holder/delete.html', context)
