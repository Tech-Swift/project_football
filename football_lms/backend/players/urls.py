from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player_list'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('player/add/', views.PlayerCreateView.as_view(), name='player_create'),
    path('player/<int:pk>/edit/', views.PlayerUpdateView.as_view(), name='player_update'),
    path('player/<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
]
