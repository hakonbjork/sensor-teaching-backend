from django.urls import path
from . import views

""" This file is responsible for listing the endpoints of the API. """

urlpatterns = [
    path('states/', views.state_view, name='state_view'),
    path('real-state/', views.get_real_state, name='get_real_state'),
    path('mock-states/', views.get_mock_states, name='get_mock_states'),
    path('clickstream/', views.add_clickstream, name='add_clickstream')
]