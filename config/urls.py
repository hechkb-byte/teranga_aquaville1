from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_views import build_admin_site

admin_site = build_admin_site()

urlpatterns = [
    path(settings.ADMIN_URL, admin_site.urls),
    path('', include('villas.urls')),
    path('services/', include('services.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
