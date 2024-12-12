import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Assuming CustomUser is your user model
from .serializers import CustomUserSerializer
from .permissions import IsAdminOrCoachOrStaff  # Assuming this permission is defined elsewhere
from .forms import UserRegisterForm, UserLoginForm

# Create a logger
logger = logging.getLogger(__name__)

# Helper function to handle common errors and form submissions
def handle_form_submission(request, form_class, success_redirect, template_name, error_message):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(success_redirect)  # Redirect on successful form submission
        else:
            return render(request, template_name, {'form': form, 'error': error_message})
    else:
        form = form_class()
    return render(request, template_name, {'form': form})

# Home view
def home(request):
    return render(request, 'index.html')

# Register view
def register(request):
    return handle_form_submission(
        request,
        UserRegisterForm,
        'accounts:login',  # Redirect to login page on successful registration
        'accounts/register.html',
        'Please correct the errors in the form'
    )

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile', user_id=request.user.id)  # If already logged in, go to profile

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']  # Get the user instance from cleaned data

            # Log the user in
            auth_login(request, user)  # Use 'auth_login' to log the user in

            # Redirect user based on their role
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            elif user.groups.filter(name='Coach').exists():
                return redirect('coach_dashboard')  # Redirect to the coach dashboard
            elif user.groups.filter(name='Staff').exists():
                return redirect('staff_dashboard')  # Redirect to the staff dashboard
            else:
                return redirect('accounts:profile', user_id=user.id)  # Default fallback to user profile

    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('accounts:login')  # Redirect to login page after logout

# Profile view
@login_required
def profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if user != request.user:
            return redirect('accounts:home')  # Redirect if trying to view someone else's profile
        return render(request, 'accounts/profile.html', {'user': user})
    except CustomUser.DoesNotExist:
        return redirect('accounts:home')  # Redirect if user not found

# Edit Profile view
@login_required
def edit_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if user != request.user:
            return redirect('accounts:home')  # Redirect if trying to edit someone else's profile

        if request.method == 'POST':
            form = UserRegisterForm(request.POST, instance=user)  # Use your existing form for editing
            if form.is_valid():
                form.save()
                return redirect('accounts:profile', user_id=user.id)
        else:
            form = UserRegisterForm(instance=user)

        return render(request, 'accounts/edit_profile.html', {'form': form})
    except CustomUser.DoesNotExist:
        return redirect('accounts:home')  # Redirect if user not found

# CustomUser view set (for API purposes)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from .permissions import IsAdminOrCoachOrStaff  # Assuming this permission is defined elsewhere

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrCoachOrStaff]  # Ensure that you have a custom permission defined

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password')

        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "password not set, missing field"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update-role')
    def update_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get('role')

        if new_role:
            user.role = new_role
            user.save()
            return Response({"status": "role updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "role not updated, missing field"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        additional_info = {
            'profile_picture': instance.profile_picture.url if instance.profile_picture else None
        }
        data = serializer.data
        data.update(additional_info)
        return Response(data)

# Role-Specific Dashboards
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrCoachOrStaff])
def admin_dashboard(request):
    return Response({'message': 'Welcome to the admin dashboard!'})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrCoachOrStaff])
def coach_dashboard(request):
    return Response({'message': 'Welcome to the coach dashboard!'})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrCoachOrStaff])
def staff_dashboard(request):
    return Response({'message': 'Welcome to the staff dashboard!'})
