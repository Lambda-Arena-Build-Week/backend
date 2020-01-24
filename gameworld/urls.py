from django.urls import path
from django.conf.urls import url

from . import api

# app_name = 'gameworld'
urlpatterns = [
    url('rooms/', api.rooms),
    url('init/', api.initialize),
    url('move/', api.move) 
]