from django.urls import path
from . import views

""" This file is responsible for listing the endpoints of the API. """

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('number/', views.number, name='number'),
    path('states/', views.state_view, name='state_view'),
    path('clickstream/', views.add_clickstream, name='add_clickstream')
]