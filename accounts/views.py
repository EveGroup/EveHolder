from django.shortcuts import render, redirect
# Create your views here.
from .models import Visitor, Event, Ticket
from .forms import TicketForm


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

def events(request):
    events = Event.objects.all()

    return render(request, 'accounts/events.html', {'events': events})

def visitors(request, pk_test):
    visitors = Visitor.objects.get(id=pk_test)
    tickets = visitors.ticket_set.all()
    tickets_count = tickets.count()

    context = {'visitors': visitors, 'tickets': tickets, 'tickets_count': tickets_count}
    return render(request, 'accounts/visitors.html', context)

def createTicket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/ticket_form.html', context)

def updateTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/ticket_form.html', context)


def deleteTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    context = {'item': ticket}
    return render(request, 'accounts/delete.html', context)
