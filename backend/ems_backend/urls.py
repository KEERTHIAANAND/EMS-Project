"""
URL configuration for ems_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({'status': 'healthy', 'message': 'EMS Backend is running'})

def api_root(request):
    """API root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to EMS Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'profile': '/api/auth/profile/',
            },
            'events': '/api/events/',
            'admin': '/admin/',
        },
        'documentation': 'Visit the endpoints above for API functionality'
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/auth/', include('authentication.urls')),
    path('api/events/', include('events.urls')),
]
