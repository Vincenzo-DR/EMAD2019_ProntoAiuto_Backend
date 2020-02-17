import json

from django.db import models

# Create your models here.
class Vettura(models.Model):
    AUTOVETTURA = 'Autovettura'
    MOTOCICLO = 'Motociclo'
    AUTOCARRO = 'Autocarro'
    ELICOTTERO = 'Elicottero'
    AMBULANZA = 'Ambulanza'
    POLIZIA = 'Polizia'
    CARABINIERI = 'Carabinieri'
    PARAMEDICI = 'Paramedici'
    POMPIERI = 'Pompieri'

    TIPOLOGIA_CHOICES = {
        AUTOVETTURA: 'Autovettura',
        MOTOCICLO: 'Motociclo',
        AUTOCARRO: 'Autocarro',
        ELICOTTERO: 'Elicottero',
        AMBULANZA: 'Ambulanza',
    }

    OPERATIVA = 'Operativa'
    NON_OPERATIVA = 'Non Operativa'

    STATO_CHOICES = {
        OPERATIVA: 'Operativa',
        NON_OPERATIVA: 'Non Operativa',
    }

    FO_CHOICES = {
        POLIZIA: 'Polizia',
        CARABINIERI: 'Carabinieri',
        PARAMEDICI: 'Paramedici',
        POMPIERI: 'Pompieri'
    }

    identificativo = models.CharField(max_length=100, unique=True)
    tipologia = models.CharField(choices=TIPOLOGIA_CHOICES.items(), max_length=100)
    forza_ordine = models.CharField(choices=FO_CHOICES.items(), max_length=100, null=True)
    stato = models.CharField(choices=STATO_CHOICES.items(), max_length=100)
    imei  = models.CharField(max_length=15)
    playerId = models.CharField(max_length=36)
    disponibile = models.BooleanField(default=True)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __str__(self):
        return self.identificativo


class Posizione(models.Model):
    long = models.CharField(max_length=20, null=True)
    lat = models.CharField(max_length=20, null=True)
    ultimo_aggiornamento = models.DateTimeField(null=True)
    vettura = models.ForeignKey(Vettura, null=True, on_delete=models.CASCADE)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __str__(self):
        return self.long + '_' + self.lat