from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Add this import
from . import views  # Import the views from the same app
from .views import CustomUserViewSet

app_name = 'accounts'  # Set the app_name for the namespace

urlpatterns = [
    # Home page route
    path('', views.home, name='home'),

    # Register and Login views
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Updated here to 'login_view'

    # Profile page route
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),    


# Logout route
    path('logout/', views.logout_view, name='logout'),  # Define the logout URL

    # JWT token endpoints for authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom User actions using ViewSets
    path('users/', views.CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', views.CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),

    # Custom user actions for password reset and role update
    path('users/<int:pk>/reset-password/', views.CustomUserViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    path('users/<int:pk>/update-role/', views.CustomUserViewSet.as_view({'put': 'update_role'}), name='update-role'),
]
