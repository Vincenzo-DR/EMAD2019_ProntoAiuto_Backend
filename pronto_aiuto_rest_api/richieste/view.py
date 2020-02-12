import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from Helper.NotifichePush import sendNotificaToCittadino
from richieste.models import Richiesta, Allegato
from richieste.forms import RichiestaCreateForm, RichiestaSupportoForm

import base64

from vetture_service.models import Vettura
from vetture_service.views import push_to_nearest


@csrf_exempt
def richieste_list(request):
    if request.method == 'GET':
        richieste = Richiesta.objects.all().values('id', 'imei', 'tipologia', 'stato', 'informazioni', 'data', 'lat',
                                                   'long', 'is_supporto', 'forza_ordine').order_by('-data')
        serialized = json.dumps(list(richieste), cls=DjangoJSONEncoder)
        return HttpResponse(serialized)
    return HttpResponseForbidden()

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
            is_supporto = form.cleaned_data['is_supporto']
            lat = form.cleaned_data['lat']
            fo = form.cleaned_data['forza_ordine']
            img_data = form.cleaned_data['img_data']
            audio_data = form.cleaned_data['audio_data']
            selfie_data = form.cleaned_data['selfie_data']
            playerID = form.cleaned_data['playerId']
            richiesta = Richiesta(imei=imei,
                                  tipologia=tipologia,
                                  stato=Richiesta.CREATA,
                                  informazioni=informazioni,
                                  data=data,
                                  is_supporto=is_supporto,
                                  linea_verde_richiesta=False,
                                  long=long,
                                  lat=lat,
                                  playerId=playerID,
                                  forza_ordine=fo
                                  )
            richiesta.save()
            if img_data:
                Allegato(file=base64_file(img_data, 'jpeg', 'fotoAllegata'), richiesta=richiesta).save()
            if audio_data:
                Allegato(file=base64_file(audio_data, 'mp3', 'audioAllegato'), richiesta=richiesta).save()
                # Allegato(file=base64_file(audio_data, 'ogg', 'audioAllegato'), richiesta=richiesta).save()
            if selfie_data:
                Allegato(file=base64_file('data:image/jpeg;base64,' + selfie_data, 'jpeg', 'selfieAllegato'), richiesta=richiesta).save()
            response = push_to_nearest(richiesta.pk, richiesta.tipologia, richiesta.lat, richiesta.long)
            print(response)
            return HttpResponse(richiesta.serialize())
    return HttpResponseForbidden()


@csrf_exempt
def crea_richiesta_supporto(request):
    if request.method == 'POST':
        form = RichiestaSupportoForm(data=request.POST)
        if form.is_valid():
            pk = form.cleaned_data['pk_req']
            imei = form.cleaned_data['imei']
            playerId = form.cleaned_data['playerId']
            fo = form.cleaned_data['forza_ordine']
            richiestaMaster=Richiesta.objects.get(id=pk)
            subRichiesta = Richiesta(imei=imei,
                                  tipologia=richiestaMaster.tipologia,
                                  stato=Richiesta.CREATA,
                                  informazioni=richiestaMaster.informazioni,
                                  data=richiestaMaster.data,
                                  is_supporto=pk,
                                  linea_verde_richiesta=False,
                                  long=richiestaMaster.long,
                                  lat=richiestaMaster.lat,
                                  playerId=playerId,
                                  forza_ordine=fo
            )
            subRichiesta.save()
            allegati = Allegato.objects.filter(richiesta=richiestaMaster)
            for a in allegati:
                a_clone = Allegato(file=a.file, richiesta=subRichiesta)
                a_clone.save()
            response = push_to_nearest(subRichiesta.pk, subRichiesta.tipologia, subRichiesta.lat, subRichiesta.long)
            print(response)
            return HttpResponse(subRichiesta.serialize())
    return HttpResponseForbidden()


@csrf_exempt
def rifiuta_richiesta(request, imei, pk_req):
    if request.method == 'GET':
        v = get_object_or_404(Vettura, imei=imei)
        v.disponibile = False
        v.save()
        r = get_object_or_404(Richiesta, pk=pk_req)
        response = push_to_nearest(r.pk, r.tipologia, r.lat, r.long)
        return HttpResponse(response)
    return HttpResponseForbidden()


@csrf_exempt
def accetta_richiesta(request, imei, pk_req):
    if request.method == 'GET':
        v = get_object_or_404(Vettura, imei=imei)
        v.disponibile = False
        v.save()
        r = get_object_or_404(Richiesta, pk=pk_req)
        r.stato = Richiesta.IN_CARICO
        r.vettura = v
        r.save()
        t_arrivo = round((r.tempoDiArrivo/60), 2)
        return HttpResponse(status=sendNotificaToCittadino(r.playerId, pk_req, t_arrivo).status_code)
    return HttpResponseForbidden()

@csrf_exempt
def completa_richiesta(request, imei, pk_req):
    if request.method == 'GET':
        v = get_object_or_404(Vettura, imei=imei)
        v.disponibile = True
        v.save()
        r = get_object_or_404(Richiesta, pk=pk_req)
        r.stato = Richiesta.RISOLTA
        r.save()
        return HttpResponse(status=200)
    return HttpResponseForbidden()

@csrf_exempt
def get_richiesta(request, pk_richiesta):
    if request.method == 'GET':
        r = Richiesta.objects.get(pk=pk_richiesta)
        return HttpResponse(r.serialize())
    return HttpResponseForbidden()\

@csrf_exempt
def get_richiesta_cittadino(request, imei):
    richieste_list = list()
    if request.method == 'GET':
        r = Richiesta.objects.filter(imei=imei, stato__in=[Richiesta.CREATA, Richiesta.IN_CARICO])
        if r.exists():
            richieste_list.append({'id': r.first().id, 'stato': r.first().stato, 'tempoDiArrivo': r.first().tempoDiArrivo})
        return HttpResponse(json.dumps(richieste_list, cls=DjangoJSONEncoder))
    return HttpResponseForbidden()

def base64_file(data, formato, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    ext = formato
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

@csrf_exempt
def get_dettaglio_richiesta(request, pk_req):
    if request.method == 'GET':
        r = Richiesta.objects.get(pk=pk_req)
        files = Allegato.objects.filter(richiesta=r)
        fotoAllegata = None
        selfieAllegato = None
        audioAllegato = None
        vetturaImei = None
        vetturaId = None
        if r.vettura:
            vetturaImei = r.vettura.imei
            vetturaId = r.vettura.identificativo
        for f in files:
            if 'selfieAllegato' in f.file.name:
                selfieAllegato = f
            elif 'fotoAllegata' in f.file.name:
                fotoAllegata = f
            elif 'audioAllegato' in f.file.name:
                audioAllegato = f

        data = {
            'imei': r.imei,
            'tipologia': r.tipologia,
            'is_supporto': r.is_supporto,
            'stato': r.stato,
            'data': r.data,
            'long': r.long,
            'lat': r.lat,
            'informazioni': r.informazioni,
            'forza_ordine': r.forza_ordine,
            'vettura': vetturaId,
            'vettura_imei': vetturaImei,
            'selfie': selfieAllegato.file.url,
            'foto': fotoAllegata.file.url,
            'audio': audioAllegato.file.url,
            'linea_verde_richiesta': r.linea_verde_richiesta,
            'tempoDiArrivo': r.tempoDiArrivo
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))
    return HttpResponseForbidden()


@csrf_exempt
def richiesta_linea_verde(request, pk_req):
    richiesta = Richiesta.objects.get(id=pk_req)
    if request.method == 'POST':
        richiesta.linea_verde_richiesta = True
        richiesta.save()
        return HttpResponse(richiesta.serialize())
    return HttpResponseForbidden()