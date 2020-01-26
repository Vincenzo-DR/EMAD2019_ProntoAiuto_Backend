import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from vetture_service.forms import VetturaCreateForm, VetturaUpdateForm
from vetture_service.models import Vettura, Posizione
from datetime import datetime


@csrf_exempt
def vetture_list(request):
    if request.method == 'GET':
        vetture = Vettura.objects.all().values('id', 'identificativo', 'tipologia', 'stato', 'imei', 'playerId')
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
                             'long': pos.long, 'ultimo_aggiornamento': pos.ultimo_aggiornamento})
        serialized = json.dumps(vett_pos, cls=DjangoJSONEncoder)
        return HttpResponse(serialized)


@csrf_exempt
def vettura_create(request):
    if request.method == 'POST':
        form = VetturaCreateForm(data=request.POST)
        if form.is_valid():
            identificativo = form.cleaned_data['identificativo']
            tipologia = form.cleaned_data['tipologia']
            imei = form.cleaned_data['imei']
            playerId = form.cleaned_data['playerId']
            vettura = Vettura(identificativo=identificativo, tipologia=tipologia, imei=imei, playerId=playerId,
                              stato=Vettura.NON_OPERATIVA)
            vettura.save()
            posizione = Posizione(long=40.955043, lat=14.275701, vettura=vettura, ultimo_aggiornamento=datetime.now())
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
            vettura.imei = form.cleaned_data['imei']
            vettura.playerId = form.cleaned_data['playerId']
            vettura.save()
            return HttpResponse(vettura.serialize())