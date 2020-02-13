import json

import requests

from richieste.models import Richiesta


def sendNotificaToFO(playerId, pk_request, tipo_request, richiesta_from):
    header = {"Content-Type": "application/json; charset=utf-8"}
    richiesta = Richiesta.objects.get(id=pk_request)
    if richiesta_from == Richiesta.RICHIESTA_DA_FO_NO_ALLEGATI:
        payload = {"app_id": "a25229e0-e3d2-419c-8706-8c0abbe60353",
                   "include_player_ids": [playerId],
                   "headings": {"en": "Nuova richiesta di soccorso"},
                   "contents": {"en": "Una voltante ha bisogno del tuo aiuto.",
                   "data": { "req_pk": pk_request, "richiesta_from": richiesta_from,
                            "lat": richiesta.lat, "long": richiesta.long }
                   }}
    else:
        payload = {"app_id": "a25229e0-e3d2-419c-8706-8c0abbe60353",
                   "include_player_ids": [playerId],
                   "headings": {"en": "Nuova richiesta di soccorso"},
                   "contents": {"en": "Emergenza per {}.".format(tipo_request)},
                   "data": {"req_pk": pk_request, "richiesta_from": richiesta_from}
                   }

    return requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))


def sendNotificaToCittadino(playerId, pk_request, tempo_di_arrivo):
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": "a25229e0-e3d2-419c-8706-8c0abbe60353",
               "include_player_ids": [playerId],
               "headings": {"en": "Richiesta presa in carico"},
               "contents": {"en": "Tempo di arrivo stimato: {} min.".format(str(tempo_di_arrivo))},
               "data": {"req_pk": pk_request}
               }

    return requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))