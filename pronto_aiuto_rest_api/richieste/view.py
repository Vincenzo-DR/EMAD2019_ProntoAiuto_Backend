from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pronto_aiuto_rest_api.richieste.models import Richiesta

@csrf_exempt
def richieste_list(request):
    if request.method == 'GET':
        richieste = Richiesta.objects.all().values('imei', 'tipologia', 'stato', 'informazioni', 'data', 'data')
        serialized = json.dumps(list(richieste), cls=DjangoJSONEncoder)
        return HttpResponse(serialized)
