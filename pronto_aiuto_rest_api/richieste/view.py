import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from richieste.models import Richiesta, Allegato
from richieste.forms import RichiestaCreateForm

import base64


@csrf_exempt
def richieste_list(request):
    if request.method == 'GET':
        richieste = Richiesta.objects.all().values('imei', 'tipologia', 'stato', 'informazioni', 'data', 'data', 'lat',
                                                   'long')
        serialized = json.dumps(list(richieste), cls=DjangoJSONEncoder)
        return HttpResponse(serialized)

@csrf_exempt
def crea_richiesta_cittadino(request):
    if request.method == 'POST':
        form = RichiestaCreateForm(data=request.POST)
        if form.is_valid():
            imei = form.cleaned_data['imei']
            tipologia = form.cleaned_data['tipologia']
            informazioni = form.cleaned_data['informazioni']
            data = str(datetime.datetime.now())
            long = form.cleaned_data['long']
            lat = form.cleaned_data['lat']
            img_data = form.cleaned_data['img_data']
            audio_data = form.cleaned_data['audio_data']
            richiesta = Richiesta(imei=imei,
                                  tipologia=tipologia,
                                  stato=Richiesta.CREATA,
                                  informazioni=informazioni,
                                  data=data,
                                  linea_verde_richiesta=False,
                                  long=long,
                                  lat=lat
                                  )
            richiesta.save()
            if img_data:
                Allegato(file=base64_file(img_data, 'fotoAllegata'), richiesta=richiesta).save()
            if audio_data:
                Allegato(file=base64_file(audio_data, 'audioAllegato'), richiesta=richiesta).save()
            return HttpResponse(richiesta.serialize())
    return HttpResponse('ASD')


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))
