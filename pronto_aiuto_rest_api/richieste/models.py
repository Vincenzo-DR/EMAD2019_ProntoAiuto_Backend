import json

from django.db import models

# Create your models here.
class Richiesta(models.Model):
    INCIDENTE = 'Incidente'
    INCENDIO = 'Incendio'
    DISSESTISTATICI = 'Dissesti statici'
    ALTRO = 'Altro'

    MOTIVO_CHOICES = {
        INCIDENTE: 'Incidente',
        INCENDIO: 'Incendio',
        DISSESTISTATICI: 'Dissesti statici',
        ALTRO: 'Altro',
    }

    CREATA = 'Creata'
    IN_CARICO = 'Presa in carico'
    RISOLTA = 'Risolta'

    STATO_CHOICES = {
        CREATA: 'Creata',
        IN_CARICO: 'Presa in carico',
        RISOLTA: 'Risolta'
    }

    imei = models.CharField(max_length=100)
    tipologia = models.CharField(choices=MOTIVO_CHOICES.items(), max_length=100, null=True)
    stato = models.CharField(choices=STATO_CHOICES.items(), max_length=100, null=True)
    informazioni = models.CharField(max_length=300, null=True)
    data = models.DateField(null=True)
    linea_verde_richiesta = models.BooleanField(default=False)
    long = models.CharField(max_length=100, null=True)
    lat = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.imei

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class Allegato(models.Model):
    richiesta = models.ForeignKey('Richiesta', on_delete=models.CASCADE)
    file = models.FileField(null=True)
