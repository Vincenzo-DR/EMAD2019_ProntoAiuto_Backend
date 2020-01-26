from django.conf.urls import url

from validators.views import check_identify

urlpatterns = [
    url(regex='^check-identify/(?P<identificativo>\w+)/$',
        view=check_identify,
        name='check-identify'),
]
