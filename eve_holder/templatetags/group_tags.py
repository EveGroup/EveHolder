"""Module for filtering group in template"""
from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check if the user is in the group_name
    Args:
        user: user to check
        group_name: name of the group to check

    Returns: True if the user is in the group_name

    """
    return user.groups.filter(name=group_name).exists()
