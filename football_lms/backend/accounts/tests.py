from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from .models import CustomUser, Role

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_role_assignment(self):
        role = Role.objects.create(role_name='coach')
        self.user.role = role
        self.user.save()
        self.assertEqual(self.user.role.role_name, 'coach')

class ViewTests(TestCase):
    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home after registration
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_login_view(self):
        user = CustomUser.objects.create_user(username='testuser', password='password')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home after login

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to login after logout

    def test_profile_view(self):
        user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Access granted to authenticated users
