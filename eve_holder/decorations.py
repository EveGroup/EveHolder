"""This module contain the decoration for users."""
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """Let all user that not register or login can use that method.

    Args:
        view_func:

    Returns:

    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('eve_holder:dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    """

    Args:
        allowed_roles:

    Returns:

    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorize to view the page!")

        return wrapper_func

    return decorator


def host_only(view_func):
    """

    Args:
        view_func:

    Returns:

    """

    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Visitors':
            return redirect('eve_holder:visitor')
        if group == 'Host':
            return view_func(request, *args, **kwargs)

    return wrapper_func
