import datetime
import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

import StringIO

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
                                                   'long', 'is_supporto', 'forza_ordine').order_by('-id')
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
            response = push_to_nearest(richiesta.pk, richiesta.tipologia, richiesta.lat, richiesta.long, Richiesta.RICHIESTA_DA_CITTADINO)
            print(response)
            return HttpResponse(richiesta.serialize())
    return HttpResponseForbidden()


@csrf_exempt
def crea_richiesta_supporto(request):
    if request.method == 'POST':
        form = RichiestaSupportoForm(data=request.POST)
        if form.is_valid():
            pk = form.cleaned_data['id_richiesta']
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
            for fl in allegati:
                tmp_file = StringIO.StringIO(fl.file.read())
                tmp_file = ContentFile(tmp_file.getvalue())
                tmp_file.name = get_file_name(fl.file.name)
                a = Allegato(file=tmp_file, richiesta=subRichiesta)
                a.save()
            response = push_to_nearest(subRichiesta.pk, subRichiesta.tipologia, subRichiesta.lat, subRichiesta.long, Richiesta.RICHIESTA_DA_FO_ALLEGATI)
            print(response)
            return HttpResponse(subRichiesta.serialize())
    return HttpResponseForbidden()


@csrf_exempt
def rifiuta_richiesta(request, imei, pk_req, richiesta_from):
    if request.method == 'GET':
        v = get_object_or_404(Vettura, imei=imei)
        v.disponibile = False
        v.save()
        r = get_object_or_404(Richiesta, pk=pk_req)
        response = push_to_nearest(r.pk, r.tipologia, r.lat, r.long, richiesta_from)
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
        vetturaIdDettaglio = None
        if r.vettura:
            vetturaImei = r.vettura.imei
            vetturaId = r.vettura.identificativo
            vetturaIdDettaglio = r.vettura.id
        for f in files:
            if 'selfieAllegato' in f.file.name:
                selfieAllegato = f.file.url
            elif 'fotoAllegata' in f.file.name:
                fotoAllegata = f.file.url
            elif 'audioAllegato' in f.file.name:
                audioAllegato = f.file.url

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
            'vetturaIdDettaglio': vetturaIdDettaglio,
            'selfie': selfieAllegato,
            'foto': fotoAllegata,
            'audio': audioAllegato,
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

def get_file_name(obj):
    string = obj
    splitted = string.split('/')
    return splitted[-1]


@csrf_exempt
def get_statistiche(request):
    if request.method == 'GET':
        richieste = Richiesta.objects.all()
        n_richieste = richieste.count()
        n_vetture = Vettura.objects.filter(stato=Vettura.OPERATIVA).count()
        n_green_line = Richiesta.objects.filter(linea_verde_richiesta=True).count()
        n_polizia = Richiesta.objects.filter(forza_ordine=Richiesta.POLIZIA).count()
        n_carabinieri = Richiesta.objects.filter(forza_ordine=Richiesta.CARABINIERI).count()
        n_pompieri = Richiesta.objects.filter(forza_ordine=Richiesta.POMPIERI).count()
        n_paramedici = Richiesta.objects.filter(forza_ordine=Richiesta.PARAMEDICI).count()
        richieste_mensili = list(richieste.extra({'month': "to_char(Date(data), 'MM')", "year": "extract(year from Date(data))"}).values('month', 'year').annotate(Count('id')))
        richieste_mensili_list = [0] * 12
        for r in richieste_mensili:
            richieste_mensili_list[int(r['month'])-1] = r['id__count']
        greenline_mensili = list(richieste.filter(linea_verde_richiesta=True).extra({'month': "to_char(Date(data), 'MM')", "year": "extract(year from Date(data))"}).values('month', 'year').annotate(Count('id')))
        greenline_mensili_list = [0] * 12
        for r in greenline_mensili:
            greenline_mensili_list[int(r['month'])-1] = r['id__count']
        tempi_di_arrivo = list(richieste.extra({'month': "to_char(Date(data), 'MM')", "year": "extract(year from Date(data))"}).values('month', 'year').annotate(Avg('tempoDiArrivo')))
        tempi_di_arrivo_list = [0] * 12
        for t in tempi_di_arrivo:
            tempi_di_arrivo_list[int(t['month'])-1] = float(format(t['tempoDiArrivo__avg']/60, '.2f'))
        data = {
            'n_richieste': n_richieste,
            'n_vetture': n_vetture,
            'n_green_line': n_green_line,
            'n_polizia': n_polizia,
            'n_carabinieri': n_carabinieri,
            'n_pompieri': n_pompieri,
            'n_paramedici': n_paramedici,
            'tempi_di_arrivo': tempi_di_arrivo_list,
            'richieste_mensili': richieste_mensili_list,
            'green_line_mensili': greenline_mensili_list
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))
    return HttpResponseForbidden()