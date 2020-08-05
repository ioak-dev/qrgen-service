from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('', views.do),
    #path('urlkey/<str:urlkey',views.get_url_key),
    path('acesskey/<str:acesskey>',views.by_key)
]