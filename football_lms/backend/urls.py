from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView

from accounts.views import CustomUserViewSet

# Initialize the DRF router
router = routers.DefaultRouter()
router.register(r'accounts/users', CustomUserViewSet)  # Updated URL for accounts users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Corrected include without namespace
    path('api/', include(router.urls)),  # Include API routes
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
