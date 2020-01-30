from richieste.models import Richiesta
from django import forms



class RichiestaCreateForm(forms.ModelForm):
    img_data = forms.CharField()
    audio_data = forms.CharField()

    class Meta:
        model = Richiesta
        fields = {'imei', 'tipologia', 'informazioni','long', 'lat'}
