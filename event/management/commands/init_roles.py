from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from event.models import Event, Category  # তোমার অ্যাপ অনুযায়ী ঠিক করো

class Command(BaseCommand):
    help = 'Create user roles and assign permissions'

    def handle(self, *args, **kwargs):
      
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        organizer_group, _ = Group.objects.get_or_create(name='Organizer')
        participant_group, _ = Group.objects.get_or_create(name='Participant')

        # Admin gets ALL permissions
        admin_group.permissions.set(Permission.objects.all())

        # Organizer permissions
        event_ct = ContentType.objects.get_for_model(Event)
        category_ct = ContentType.objects.get_for_model(Category)

        organizer_perms = Permission.objects.filter(
            content_type__in=[event_ct, category_ct],
            codename__in=[
                'add_event', 'change_event', 'delete_event',
                'add_category', 'change_category', 'delete_category'
            ]
        )
        organizer_group.permissions.set(organizer_perms)

        self.stdout.write(self.style.SUCCESS('Admin, Organizer, Participant roles created with appropriate permissions.'))
