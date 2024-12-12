from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CustomUserViewSet, admin_dashboard, coach_dashboard, staff_dashboard

app_name = 'accounts'

urlpatterns = [
    # Home page route
    path('', views.home, name='home'),

    # Register and Login views
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # Profile page route
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),

    # Logout route
    path('logout/', views.logout_view, name='logout'),

    # JWT token endpoints for authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom User actions using ViewSets
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),

    # Custom user actions for password reset and role update
    path('users/<int:pk>/reset-password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    path('users/<int:pk>/update-role/', CustomUserViewSet.as_view({'put': 'update_role'}), name='update-role'),

    # Custom user dashboard views (standalone functions, not ViewSet methods)
    path('users/<int:pk>/admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('users/<int:pk>/coach-dashboard/', coach_dashboard, name='coach_dashboard'),
    path('users/<int:pk>/staff-dashboard/', staff_dashboard, name='staff_dashboard'),
]
