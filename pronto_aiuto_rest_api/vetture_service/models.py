import json

from django.db import models

# Create your models here.
class Vettura(models.Model):
    AUTOVETTURA = 'Autovettura'
    MOTOCICLO = 'Motociclo'
    CORAZZATO = 'Corazzato'
    ELICOTTERO = 'Elicottero'
    AMBULANZA = 'Ambulanza'

    TIPOLOGIA_CHOICES = {
        AUTOVETTURA: 'Autovettura',
        MOTOCICLO: 'Motociclo',
        CORAZZATO: 'Corazzato',
        ELICOTTERO: 'Elicottero',
        AMBULANZA: 'Ambulanza',
    }

    OPERATIVA = 'Operativa'
    NON_OPERATIVA = 'Non Operativa'

    STATO_CHOICES = {
        OPERATIVA: 'Operativa',
        NON_OPERATIVA: 'Non Operativa',
    }

    identificativo = models.CharField(max_length=100, unique=True)
    tipologia = models.CharField(choices=TIPOLOGIA_CHOICES.items(), max_length=100)
    stato = models.CharField(choices=STATO_CHOICES.items(), max_length=100)
    imei  = models.CharField(max_length=15)
    playerId = models.CharField(max_length=36)
    disponibile = models.BooleanField(default=True)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __str__(self):
        return self.identificativo


class Posizione(models.Model):
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    ultimo_aggiornamento = models.DateTimeField(null=True)
    vettura = models.ForeignKey(Vettura, null=True, on_delete=models.CASCADE)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __str__(self):
        return self.long + '_' + self.lat