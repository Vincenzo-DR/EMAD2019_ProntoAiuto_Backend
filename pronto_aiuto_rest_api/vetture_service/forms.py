from django import forms

from vetture_service.models import Vettura, Posizione


class VetturaCreateForm(forms.ModelForm):
    class Meta:
        model = Vettura
        fields = {'identificativo', 'tipologia', 'imei', 'playerId', 'stato', 'forza_ordine'}

class VetturaUpdateForm(forms.ModelForm):
    class Meta:
        model = Vettura
        fields = {'tipologia', 'imei', 'playerId', 'stato', 'forza_ordine'}

class PosizioneUpdateForm(forms.ModelForm):
    class Meta:
        model = Posizione
        fields = {'lat', 'long'}