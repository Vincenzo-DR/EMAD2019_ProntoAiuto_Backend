from django.conf.urls import url
from vetture_service.views import vetture_list, vettura_delete, vettura_create, vettura_update, vetture_list_position, \
    update_position, updateDisponibilita, get_dettaglio_vettura, get_disponibilita_vettura

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
    url(regex='^update-disp/(?P<imei>\w+)/$',
        view=updateDisponibilita,
        name='update_disp'),
    url(regex='^get/vettura/details/(?P<pk_vet>[0-9]+)/$',
        view=get_dettaglio_vettura,
        name='get_dettaglio_vettura'),
    url(regex='^get-disp/(?P<imei>\w+)/$',
        view=get_disponibilita_vettura,
        name='get_disp'),

]
