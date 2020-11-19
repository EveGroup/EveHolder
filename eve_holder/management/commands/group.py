from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


def group_strategy(group_name: str, group_permission: list):
    try:
        group = Group.objects.get(name=group_name)
        group.save()
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name)
        group.permissions.set(group_permission)
        group.save()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument()

    def handle(self, *args, **options):
        host_perm_names = ['Can add event', 'Can change event', 'Can delete event', 'Can view event', 'Can change host',
                           'Can view visitor']
        visitor_perm_names = ['Can add event', 'Can change event', 'Can delete event', 'Can view event',
                              'Can add session', 'Can change session', 'Can delete session', 'Can view session']
        host_permissions = [Permission.objects.get(name=name) for name in host_perm_names]
        visitors_permissions = [Permission.objects.get(name=name) for name in visitor_perm_names]
        group_strategy("Host", host_permissions)
        group_strategy("Visitors", visitors_permissions)
