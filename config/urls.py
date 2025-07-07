from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth.views import LoginView

schema_view = get_schema_view(
    openapi.Info(
        title="Movie recommendation service",
        default_version='v0.1',
        description="Rate and get recommendations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="koltyrin.art@yandex.ru", name="Artur"),
        license=openapi.License(name="BSD License"),),
    public=True,
    permission_classes=[permissions.AllowAny,])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('movies.urls', namespace='movies')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)