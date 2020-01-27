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

    imei = models.CharField(max_length=100, unique=True)
    tipologia = models.CharField(choices=MOTIVO_CHOICES.items(), max_length=100, null=True)
    stato = models.CharField(choices=STATO_CHOICES.items(), max_length=100, null=True)
    informazioni = models.CharField(max_length=300, null=True)
    data = models.DateField(null=True)
    linea_verde_richiesta = models.BooleanField(default=False)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return self.imei

class Allegato(models.Model):
    richiesta = models.ForeignKey('Richiesta')
    file = models.FileField(null=True)
