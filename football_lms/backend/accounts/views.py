from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout  # Import the logout function
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser  # Import the CustomUser model first
from .serializers import CustomUserSerializer
from .permissions import IsAdminOrCoachOrStaff  # Assuming this permission is defined elsewhere
from .forms import UserRegisterForm, UserLoginForm

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
        'login',  # Redirect to login page on successful registration
        'accounts/register.html',
        'Please correct the errors in the form'
    )

# Login view
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page on successful login
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Please correct the errors in the form'})
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to login page after logout

# CustomUser view set
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrCoachOrStaff]

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
