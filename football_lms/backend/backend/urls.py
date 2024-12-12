from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts.views import CustomUserViewSet, home  # Import the home view directly
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'accounts/users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Corrected include without namespace
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/players/', include('players.urls')),
    path('', home, name='home'),  # Updated to link directly to the home view
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
