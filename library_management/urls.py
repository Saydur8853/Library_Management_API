from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from drf_spectacular.utils import extend_schema
from .serializers import APIRootResponseSerializer

def redirect_to_api(request):
    return redirect('/api/')

@extend_schema(
    operation_id='api_root',
    summary='API Root',
    description='Welcome to the Library Management API. Returns available endpoints and documentation links.',
    responses={
        200: APIRootResponseSerializer,
    },
    tags=['API Root']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Library Management API Root
    
    Welcome to the Library Management API. Below are the available endpoints:
    """
    return Response({
        'message': 'Welcome to Library Management API',
        'endpoints': {
            'authentication': {
                'register': request.build_absolute_uri('/api/register/'),
                'login': request.build_absolute_uri('/api/login/'),
            },
            'library': {
                'authors': request.build_absolute_uri('/api/authors/'),
                'categories': request.build_absolute_uri('/api/categories/'),
                'books': request.build_absolute_uri('/api/books/'),
                'borrow': request.build_absolute_uri('/api/borrow/'),
                'my_borrows': request.build_absolute_uri('/api/my-borrows/'),
                'return': request.build_absolute_uri('/api/return/'),
            }
        },
        'admin': request.build_absolute_uri('/admin/'),
        'documentation': {
            'swagger_ui': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'openapi_schema': request.build_absolute_uri('/api/schema/'),
            'browsable_api': 'Navigate to any endpoint above to see the DRF browsable API interface'
        }
    })

urlpatterns = [
    path('', redirect_to_api),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/', api_root, name='api-root'),
    path('api/', include('authentication.urls')),
    path('api/', include('books.urls')),
]
