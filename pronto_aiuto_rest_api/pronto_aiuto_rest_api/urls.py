from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'vetture/', include('vetture_service.urls')),
    url(r'validators/', include('validators.urls')),
    url(r'richiesta/', include('richieste.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)