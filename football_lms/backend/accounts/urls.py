from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views  # Import the views from the same app
from .views import CustomUserViewSet

app_name = 'accounts'  # Set the app_name for the namespace

urlpatterns = [
    path('', views.home, name='home'),  # Home page route
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom User actions
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
]
