from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_migrate)
def assign_permissions(sender, **kwargs):
    user_content_type = ContentType.objects.get_for_model(CustomUser)

    # Get permissions for the CustomUser model
    view_permission = Permission.objects.get(codename='view_user', content_type=user_content_type)
    add_permission = Permission.objects.get(codename='add_user', content_type=user_content_type)
    change_permission = Permission.objects.get(codename='change_user', content_type=user_content_type)
    delete_permission = Permission.objects.get(codename='delete_user', content_type=user_content_type)

    # Create groups and assign permissions
    admin_group, created = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.set([view_permission, add_permission, change_permission, delete_permission])

    coach_group, created = Group.objects.get_or_create(name='Coach')
    coach_group.permissions.set([view_permission, change_permission])  # Limited permissions

    staff_group, created = Group.objects.get_or_create(name='Staff')
    staff_group.permissions.set([view_permission])  # View-only permissions
