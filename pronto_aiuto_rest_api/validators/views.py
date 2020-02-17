from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from vetture_service.models import Vettura


@csrf_exempt
def check_identify(request, identificativo):
    if request.method == 'GET':
        vettura = get_object_or_404(Vettura, identificativo=identificativo)
        return HttpResponse(vettura.serialize())