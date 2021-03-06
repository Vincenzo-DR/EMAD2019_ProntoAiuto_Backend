import json
import os
from datetime import datetime

from django.db import models

# Create your models here.
from vetture_service.models import Vettura

class Richiesta(models.Model):
    INCIDENTE_STRADALE = 'Incidente stradale'
    INCIDENTE = 'Incidente'
    INCENDIO = 'Incendio'
    DISSESTISTATICI = 'Dissesti statici'
    FURTO = 'Furto'
    VIOLENZADOMESTICA = 'Violenza domestica'
    MALOREIMPROVVISO = 'Malore improvviso'
    ALTRO = 'Altro'
    TRUE = 'True'
    FALSE = 'False'
    CREATA = 'Creata'
    IN_CARICO = 'Presa in carico'
    RISOLTA = 'Risolta'
    POLIZIA = 'Polizia'
    CARABINIERI = 'Carabinieri'
    PARAMEDICI = 'Paramedici'
    POMPIERI = 'Pompieri'
    SUPPORTO= 'Supporto'

    RICHIESTA_DA_CITTADINO = 1
    RICHIESTA_DA_FO_NO_ALLEGATI = 2
    RICHIESTA_DA_FO_ALLEGATI = 3

    MOTIVO_CHOICES = {
        INCIDENTE_STRADALE: 'Incidente stradale',
        INCIDENTE: 'Incidente',
        INCENDIO: 'Incendio',
        DISSESTISTATICI: 'Dissesti statici',
        FURTO: 'Furto',
        VIOLENZADOMESTICA: 'Violenza domestica',
        MALOREIMPROVVISO: 'Malore improvviso',
        ALTRO: 'Altro',
        SUPPORTO: 'Supporto'
    }

    STATO_CHOICES = {
        CREATA: 'Creata',
        IN_CARICO: 'Presa in carico',
        RISOLTA: 'Risolta'
    }

    FO_CHOICES = {
        POLIZIA: 'Polizia',
        CARABINIERI: 'Carabinieri',
        PARAMEDICI: 'Paramedici',
        POMPIERI: 'Pompieri'
    }

    imei = models.CharField(max_length=100)
    tipologia = models.CharField(choices=MOTIVO_CHOICES.items(), max_length=100, null=True)
    forza_ordine = models.CharField(choices=FO_CHOICES.items(), max_length=100, null=True)
    is_supporto = models.CharField(max_length=100, null=True, default=None)
    stato = models.CharField(choices=STATO_CHOICES.items(), max_length=100, null=True)
    informazioni = models.CharField(max_length=300, null=True)
    data = models.CharField(null=True, max_length=100)
    linea_verde_richiesta = models.BooleanField(default=False)
    long = models.CharField(max_length=100, null=True)
    lat = models.CharField(max_length=100, null=True)
    vettura = models.ForeignKey(Vettura, on_delete=models.CASCADE, null=True, default=None)
    playerId = models.CharField(max_length=36, null=False, default='')
    tempoDiArrivo = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.imei

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def content_file_name(instance, filename):
    year = datetime.utcnow().strftime("%Y")
    month = datetime.utcnow().strftime("%B")
    richiesta = str(instance.richiesta.id)
    return os.sep.join([year, month, richiesta, filename])


class Allegato(models.Model):
    richiesta = models.ForeignKey('Richiesta', on_delete=models.CASCADE)
    file = models.FileField(null=True,  upload_to=content_file_name, max_length=500)
