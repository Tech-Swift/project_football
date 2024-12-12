from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_migrate)
def assign_permissions(sender, **kwargs):
    user_content_type = ContentType.objects.get_for_model(CustomUser)

    # Create permissions if they don't exist
    view_permission, created = Permission.objects.get_or_create(
        codename='view_user',
        name='Can view user',
        content_type=user_content_type,
    )
    add_permission, created = Permission.objects.get_or_create(
        codename='add_user',
        name='Can add user',
        content_type=user_content_type,
    )
    change_permission, created = Permission.objects.get_or_create(
        codename='change_user',
        name='Can change user',
        content_type=user_content_type,
    )
    delete_permission, created = Permission.objects.get_or_create(
        codename='delete_user',
        name='Can delete user',
        content_type=user_content_type,
    )

    # Create groups and assign permissions
    admin_group, created = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.set([view_permission, add_permission, change_permission, delete_permission])

    coach_group, created = Group.objects.get_or_create(name='Coach')
    coach_group.permissions.set([view_permission, change_permission])  # Limited permissions

    staff_group, created = Group.objects.get_or_create(name='Staff')
    staff_group.permissions.set([view_permission])  # View-only permissions
