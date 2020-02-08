import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from Helper.NotifichePush import sendNotificaToFO
from richieste.models import Richiesta
from vetture_service.forms import VetturaCreateForm, VetturaUpdateForm, PosizioneUpdateForm, VetturaUpdateDisponibilita
from vetture_service.models import Vettura, Posizione
from datetime import datetime

import requests

@csrf_exempt
def vetture_list(request):
    if request.method == 'GET':
        vetture = Vettura.objects.all().values('id', 'identificativo', 'tipologia', 'stato', 'imei', 'playerId', 'forza_ordine', 'disponibile')
        serialized = json.dumps(list(vetture), cls=DjangoJSONEncoder)
        return HttpResponse(serialized)

@csrf_exempt
def vetture_list_position(request):
    if request.method == 'GET':
        vett_pos = list()
        vetture = Vettura.objects.all()
        for vet in vetture:
            pos = Posizione.objects.get(vettura=vet)
            vett_pos.append({'id': vet.id, 'identificativo': vet.identificativo, 'tipologia': vet.tipologia,
                             'stato': vet.stato, 'imei': vet.imei, 'playerId': vet.playerId, 'lat': pos.lat,
                             'long': pos.long, 'ultimo_aggiornamento': pos.ultimo_aggiornamento,
                             'disponibile': vet.disponibile, 'forza_ordine': vet.forza_ordine})
        serialized = json.dumps(vett_pos, cls=DjangoJSONEncoder)
        return HttpResponse(serialized)


@csrf_exempt
def vettura_create(request):
    if request.method == 'POST':
        form = VetturaCreateForm(data=request.POST)
        if form.is_valid():
            identificativo = form.cleaned_data['identificativo']
            tipologia = form.cleaned_data['tipologia']
            stato = form.cleaned_data['stato']
            imei = form.cleaned_data['imei']
            playerId = form.cleaned_data['playerId']
            fo = form.cleaned_data['forza_ordine']
            vettura = Vettura(identificativo=identificativo, tipologia=tipologia, imei=imei, playerId=playerId,
                              stato=stato, forza_ordine=fo)
            vettura.save()
            posizione = Posizione(long="", lat="", vettura=vettura, ultimo_aggiornamento=datetime.now())
            posizione.save()
            return HttpResponse(vettura.serialize())

@csrf_exempt
def vettura_delete(request, pk):
    if request.method == 'DELETE':
        vettura = get_object_or_404(Vettura, pk=pk)
        vettura.delete()
        return HttpResponse()

@csrf_exempt
def vettura_update(request, pk):
    vettura = get_object_or_404(Vettura, pk=pk)
    if request.method == 'GET':
        return HttpResponse(vettura.serialize())
    elif request.method == 'POST':
        form = VetturaUpdateForm(data=request.POST)
        if form.is_valid():
            vettura.tipologia = form.cleaned_data['tipologia']
            vettura.stato = form.cleaned_data['stato']
            vettura.imei = form.cleaned_data['imei']
            vettura.playerId = form.cleaned_data['playerId']
            vettura.forza_ordine = form.cleaned_data['forza_ordine']
            vettura.save()
            return HttpResponse(vettura.serialize())

@csrf_exempt
def update_position(request, imei):
    vettura = get_object_or_404(Vettura, imei=imei)
    posizione = get_object_or_404(Posizione, vettura=vettura)
    if request.method == 'POST':
        form = PosizioneUpdateForm(data=request.POST)
        if form.is_valid():
            posizione.lat = form.cleaned_data['lat']
            posizione.long = form.cleaned_data['long']
            posizione.save()
            return HttpResponse(status=200)


def push_to_nearest(pk_request, tipo_request, lat_req, long_req):
    lat_end = lat_req
    long_end = long_req
    times_of_arrival = {}
    req = get_object_or_404(Richiesta, pk=pk_request)
    vetture = Vettura.objects.filter(stato=Vettura.OPERATIVA, disponibile=True, forza_ordine=req.forza_ordine)
    for vet in vetture:
        lat_start = Posizione.objects.get(vettura=vet).lat
        long_start = Posizione.objects.get(vettura=vet).long
        r = requests.get('https://api.tomtom.com/routing/1/calculateRoute/{}%2C{}%3A{}%2C{}/json?computeTravelTimeFor=all&routeType=fastest&traffic=true&avoid=unpavedRoads&travelMode=car&key=pBDtSNH15AVCe1kLOKb1lgvdgWtGCHaG'.format(lat_start, long_start, lat_end, long_end))
        seconds = (r.json()['routes'][0]['summary']['travelTimeInSeconds'])
        times_of_arrival.update({vet.playerId: int(seconds)})
    playerId = min(times_of_arrival, key=times_of_arrival.get)
    req.tempoDiArrivo = times_of_arrival.get(playerId)
    req.save()
    return sendNotificaToFO(playerId, pk_request, tipo_request).status_code

@csrf_exempt
def updateDisponibilita(request, imei):
    vettura = get_object_or_404(Vettura, imei=imei)
    form = VetturaUpdateDisponibilita(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            disponibile = form.cleaned_data['disponibile']
            vettura.disponibile = disponibile
            vettura.save()
            if(disponibile):
                richieste = Richiesta.objects.filter(vettura=vettura)
                for r in richieste:
                    if r.stato != r.RISOLTA:
                        r.stato = r.RISOLTA
                        r.save()
            return HttpResponse(vettura.serialize())


@csrf_exempt
def get_disponibilita_vettura(request, imei):
    if request.method == 'GET':
        v = Vettura.objects.get(imei=imei)
        data = {
            'disponibile': v.disponibile,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))
    return HttpResponseForbidden()

