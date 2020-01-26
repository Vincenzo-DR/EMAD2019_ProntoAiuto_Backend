from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'vetture/', include('vetture_service.urls')),
    url(r'validators/', include('validators.urls'))
]