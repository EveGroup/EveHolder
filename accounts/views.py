from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Visitor, Event, Ticket
from .forms import TicketForm, CreateUserForm
from .filters import TicketFilter


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
    tickets = Ticket.objects.all()

    total_tickets = tickets.count()
    available_count = tickets.filter(status='Available').count()
    reserved_count = tickets.filter(status='Reserved').count()

    context = {'visitors': visitors, 'tickets': tickets,
               'total_tickets': total_tickets, 'available_count': available_count,
               'reserved_count': reserved_count}
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
def events(request):
    events = Event.objects.all()
    return render(request, 'accounts/events.html', {'events': events})


@login_required(login_url='login')
def visitors(request, pk):
    visitors = Visitor.objects.get(id=pk)
    tickets = visitors.ticket_set.all()
    tickets_count = tickets.count()

    my_filter = TicketFilter(request.GET, queryset=tickets)
    tickets = my_filter.qs

    context = {'visitors': visitors, 'tickets': tickets,
               'tickets_count': tickets_count, 'my_filter': my_filter
               }
    return render(request, 'accounts/visitors.html', context)


@login_required(login_url='login')
def create_ticket(request, pk):
    visitors = Visitor.objects.get(id=pk)
    form = TicketForm(initial={'visitor': visitors})
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/ticket_form.html', context)


@login_required(login_url='login')
def update_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/ticket_form.html', context)


@login_required(login_url='login')
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    context = {'item': ticket}
    return render(request, 'accounts/delete.html', context)
