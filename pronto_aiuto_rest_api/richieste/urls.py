from django.conf.urls import url

from pronto_aiuto_rest_api.richieste.view import richieste_list, crea_richiesta_cittadino

urlpatterns = [
    url(regex='^list/$',
        view=richieste_list,
        name='richieste_list'),
    url(regex='^create/$',
        view=crea_richiesta_cittadino,
        name='richiesta_create'),
]
