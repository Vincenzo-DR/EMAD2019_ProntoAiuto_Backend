from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from pronto_aiuto_rest_api.richieste.models import Richiesta
from pronto_aiuto_rest_api.richieste.forms import RichiestaCreateForm


@csrf_exempt
def richieste_list(request):
    if request.method == 'GET':
        richieste = Richiesta.objects.all().values('imei', 'tipologia', 'stato', 'informazioni', 'data', 'data')
        serialized = json.dumps(list(richieste), cls=DjangoJSONEncoder)
        return HttpResponse(serialized)

@csrf_exemp
def crea_richiesta_cittadino(request):
    if request.method == 'POST':
        form = RichiestaCreateForm(data=request.POST)
        if form.is_valid():
            imei = form.cleaned_data['imei']
            tipologia = form.cleaned_data['tipologia']
            informazioni = form.cleaned_data['informazioni']
            data = form.cleaned_data['data']
            long = form.cleaned_data['long']
            lat = form.cleaned_data['lat']
            richiesta = Richiesta(  imei=imei,
                                    tipologia=tipologia,
                                    stato=Richiesta.CREATA,
                                    informazioni=informazioni,
                                    data=data,
                                    linea_verde_richiesta=False,
                                    long=long,
                                    lat=lat
                                    )
            richiesta.save()
            return HttpResponse(richiesta.serialize())