from django import template
from django.urls import reverse

register = template.Library()

@register.inclusion_tag('accounts/navbar.html')
def render_navbar(user):
    """
    Render the navbar with links based on whether the user is authenticated
    """
    if user.is_authenticated:
        return {
            'profile_url': reverse('accounts:profile', args=[user.id]),
            'logout_url': reverse('accounts:logout'),
            'dashboard_url': get_dashboard_url(user),
            'players_url': reverse('players:player_list'),
            'authenticated': True,
        }
    return {
        'login_url': reverse('accounts:login'),
        'register_url': reverse('accounts:register'),
        'authenticated': False,
    }

def get_dashboard_url(user):
    """
    Return the appropriate dashboard URL based on the user's group
    """
    if user.groups.filter(name='Admin').exists():
        return reverse('accounts:admin_dashboard')
    elif user.groups.filter(name='Coach').exists():
        return reverse('accounts:coach_dashboard')
    elif user.groups.filter(name='Staff').exists():
        return reverse('accounts:staff_dashboard')
    return ''
