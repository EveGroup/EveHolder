from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Visitor, Event
from .forms import EventForm, CreateUserForm
from .filters import EventFilter


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
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
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    visitors = Visitor.objects.all()
    events = Event.objects.all()

    total_events = events.count()

    context = {'visitors': visitors, 'events': events, 'total_events': total_events}
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
def events(request):
    events = Event.objects.all()
    return render(request, 'accounts/events.html', {'events': events})


@login_required(login_url='login')
def visitors(request, pk):
    visitors = Visitor.objects.get(id=pk)
    events = visitors.event_set.all()
    events_count = events.count()

    my_filter = EventFilter(request.GET, queryset=events)
    events = my_filter.qs

    context = {'visitors': visitors, 'events': events,
               'events_count': events_count, 'my_filter': my_filter
               }
    return render(request, 'accounts/visitors.html', context)


@login_required(login_url='login')
def create_event(request, pk):
    visitors = Visitor.objects.get(id=pk)
    form = EventForm(initial={'visitor': visitors})
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/event_form.html', context)


@login_required(login_url='login')
def edit_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/event_form.html', context)


@login_required(login_url='login')
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    context = {'item': event}
    return render(request, 'accounts/delete.html', context)
