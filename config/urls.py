"""
URL configuration for the internet-shop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Главная страница API
def api_root(request):
    return JsonResponse({
        'auth': '/api/auth/',
        'products': '/api/products/',
        'cart': '/api/cart/',
        'orders': '/api/orders/',
        'schema': '/api/schema/',
        'swagger-ui': '/api/schema/swagger-ui/',
        'redoc': '/api/schema/redoc/',
    })

urlpatterns = [
    path('admin/', admin.site.urls),

    # Корень API
    path('api/', api_root, name='api-root'),

    # Подмаршруты API
    path('api/auth/', include('app.users.urls')),
    path('api/products/', include('app.products.urls')),
    path('api/cart/', include('app.cart.urls')),
    path('api/orders/', include('app.orders.urls')),

    # API schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Статика и медиа (только в DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)