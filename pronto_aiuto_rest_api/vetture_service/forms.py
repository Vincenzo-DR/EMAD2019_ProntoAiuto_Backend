from django import forms

from vetture_service.models import Vettura


class VetturaCreateForm(forms.ModelForm):
    class Meta:
        model = Vettura
        fields = {'identificativo', 'tipologia', 'imei', 'playerId'}

class VetturaUpdateForm(forms.ModelForm):
    class Meta:
        model = Vettura
        fields = {'tipologia', 'imei', 'playerId'}