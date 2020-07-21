from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import app.auth.service as service
from django.core import serializers
import json

@api_view(['GET'])
def jwtTest(request, tenant):
    response = service.do_jwttest(tenant)
    return HttpResponse(response[1], status=response[0])

@api_view(['POST'])
def signin_jwt(request, tenant):
    response = service.do_signin_via_jwt(tenant, request.body)
    return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def get_session(request, tenant, auth_key):
    print("*****************")
    print(auth_key)
    response = service.get_session(tenant, auth_key)
    return JsonResponse(response[1], status=response[0])
