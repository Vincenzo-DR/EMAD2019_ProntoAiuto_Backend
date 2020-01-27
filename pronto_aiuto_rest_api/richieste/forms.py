from richieste.models import Richiesta
from django import forms



class RichiestaCreateForm(forms.ModelForm):
    class Meta:
        model = Richiesta
        fields = {'imei', 'tipologia', 'informazioni','long', 'lat'}
