from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.crisis_map, name='crisis_map'),
]
