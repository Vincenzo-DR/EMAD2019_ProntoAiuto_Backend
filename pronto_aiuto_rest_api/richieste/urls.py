from django.conf.urls import url

from richieste.view import richieste_list, crea_richiesta_cittadino, rifiuta_richiesta, accetta_richiesta, \
    get_richiesta, completa_richiesta, get_richiesta_cittadino, \
    get_dettaglio_richiesta, richiesta_linea_verde, get_statistiche, crea_richiesta_supporto

urlpatterns = [
    url(regex='^list/$',
        view=richieste_list,
        name='richieste_list'),
    url(regex='^create/$',
        view=crea_richiesta_cittadino,
        name='richiesta_create'),
    url(regex='^create-supporto/$',
        view=crea_richiesta_supporto,
        name='richiesta_create_supporto'),
    url(regex='^rifiuta/(?P<imei>\w+)/(?P<pk_req>[0-9]+)/(?P<richiesta_from>[0-9]+)/$',
        view=rifiuta_richiesta,
        name='rifiuta_richiesta'),
    url(regex='^accetta/(?P<imei>\w+)/(?P<pk_req>[0-9]+)/$',
        view=accetta_richiesta,
        name='accetta_richiesta'),
    url(regex='^completa/(?P<imei>\w+)/(?P<pk_req>[0-9]+)/$',
        view=completa_richiesta,
        name='completa_richiesta'),
    url(regex='^get/(?P<pk_req>[0-9]+)/$',
        view=get_richiesta,
        name='get_richiesta'),
    url(regex='^get/cittadino/(?P<imei>\w+)/$',
        view=get_richiesta_cittadino,
        name='get_richiesta_cittadino'),
    url(regex='^get/richiesta/detail/(?P<pk_req>[0-9]+)/$',
        view=get_dettaglio_richiesta,
        name='get_richiesta_dettaglio'),
    url(regex='^richiesta-linea-verde/(?P<pk_req>[0-9]+)/$',
        view=richiesta_linea_verde,
        name='richiesta_linea_verde'),
    url(regex='^get_statistiche/$',
        view=get_statistiche,
        name='get_statistiche'),

]
