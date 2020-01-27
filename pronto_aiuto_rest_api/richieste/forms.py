from pronto_aiuto_rest_api.richieste.models import Richiesta


class RichiestaCreateForm(forms.ModelForm):
    class Meta:
        model = Richiesta
        fields = {'imei', 'tipologia', 'stato', 'informazioni', 'data', 'linea_verde_richiesta', 'long', 'lat'}
