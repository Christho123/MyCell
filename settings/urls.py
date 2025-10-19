from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Importa settings
from django.conf.urls.static import static  # Importa static
from django.http import JsonResponse

def health_check(request):
    """Endpoint de health check para Docker"""
    return JsonResponse({'status': 'healthy', 'service': 'reflexo-backend'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    
    path('api/', include([
        path('architect/', include('architect.urls')),
        
        path('profiles/', include('users_profiles.urls')),

        path('employees/', include('employees.urls')),

        path('locations/', include('ubi_geo.urls')),

        path('types/', include('app_types.urls')),

    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
