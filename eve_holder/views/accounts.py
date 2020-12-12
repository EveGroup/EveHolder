from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from eve_holder.decorations import unauthenticated_user
from eve_holder.forms import CreateUserForm
from eve_holder.models import Visitor, Host


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
        # fill the form with information from POST data
        # which Main model is User
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # get the cleaned data from the form for creating Visitor and Host objects
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone_num = request.POST.get('phone_number')
            group_name = request.POST.get('type')

            # add group to User [Host, Visitor]
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

        # check if the user is valid (if there is no user with this username & password return None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group = request.user.groups.all()[0].name
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