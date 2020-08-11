from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.url.service as service

@api_view(['POST'])
def do(request):
    if request.method == 'POST':
        response = service.create(request)
        return JsonResponse(response[1], status=response[0])

#@api_view(['GET'])
#def get_url_key(request,tenant,urlkey):
 #   if request.method == 'GET':
  #      response = service.find_all(request, tenant,urlkey)
   #     return JsonResponse(response[1], status=response[0])

#@api_view(['GET''PUT', 'DELETE'])
#def by_key(request,acesskey):
 #   if request.method =='GET':
  #      response = service.find__by_key(request,acesskey)
  #      return JsonResponse(response[1], status=response[0])
   # elif request.method =='PUT':
   #     response = service.update_by_key(request,acesskey)
   #     return JsonResponse(response[1], status=response[0])
   # else:
   #     request.method =='DELETE'
   #     response = service.delete_by_key(request,acesskey)
    #    return  JsonResponse(response[1],status=response[0])
