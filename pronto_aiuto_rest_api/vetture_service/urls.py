from django.conf.urls import url
from vetture_service.views import vetture_list, vettura_delete, vettura_create, vettura_update, vetture_list_position, \
    update_position

urlpatterns = [
    url(regex='^list/$',
        view=vetture_list,
        name='vetture_list'),
    url(regex='^list-vetture-position/$',
        view=vetture_list_position,
        name='vetture_list_position'),
    url(regex='^create/$',
        view=vettura_create,
        name='vettura_create'),
    url(regex='^delete/(?P<pk>[0-9]+)/$',
        view=vettura_delete,
        name='vettura_delete'),
    url(regex='^update/(?P<pk>[0-9]+)/$',
        view=vettura_update,
        name='vettura_update'),
    url(regex='^update-position/(?P<imei>\w+)/$',
        view=update_position,
        name='update_position'),
]
