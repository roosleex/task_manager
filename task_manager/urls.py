from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin_url1 = settings.ADMIN_URL1

urlpatterns = [
    path(admin_url1 + '/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls')),
    path('', include('mainapp.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

