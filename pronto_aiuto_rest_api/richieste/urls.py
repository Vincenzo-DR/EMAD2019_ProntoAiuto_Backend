from django.conf.urls import url

from richieste.view import richieste_list, crea_richiesta_cittadino, rifiuta_richiesta, accetta_richiesta

urlpatterns = [
    url(regex='^list/$',
        view=richieste_list,
        name='richieste_list'),
    url(regex='^create/$',
        view=crea_richiesta_cittadino,
        name='richiesta_create'),
    url(regex='^rifiuta/(?P<imei>\w+)/(?P<pk_req>[0-9]+)/$',
        view=rifiuta_richiesta,
        name='rifiuta_richiesta'),
    url(regex='^accetta/(?P<imei>\w+)/(?P<pk_req>[0-9]+)/$',
        view=accetta_richiesta,
        name='accetta_richiesta'),
]
