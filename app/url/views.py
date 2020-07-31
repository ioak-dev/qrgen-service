from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.url.service as service

@api_view(['GET', 'PUT'])
def do(request):
    if request.method == 'GET':
        response = service.find_all(request)
        return JsonResponse(response[1], status=response[0])
    elif request.method == 'PUT':
        response = service.update_url(request)
        return JsonResponse(response[1], status=response[0])
