from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CustomUserSerializer
from .permissions import IsAdminOrCoachOrStaff  # Assuming this permission is defined elsewhere

# Define the CustomUser model
class CustomUser(AbstractUser):
    # Add any extra fields here
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

# Use get_user_model() to dynamically get the CustomUser model
CustomUser = get_user_model()

# Define the home view
def home(request):
    return render(request, 'index.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Redirect to the login page after registration
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page or desired URL after login
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('accounts:login')  # Redirect to the login page after logout

# CustomUser view set
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrCoachOrStaff]  # Ensure permission checks are in place

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
        # Override the default retrieve method to include additional data
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Assuming 'profile_picture' is a field in your CustomUser model
        additional_info = {
            'profile_picture': instance.profile_picture.url if instance.profile_picture else None
        }
        data = serializer.data
        data.update(additional_info)
        return Response(data)
