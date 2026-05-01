from django.urls import path
from . import views

urlpatterns = [
    path('crisis/<int:crisis_pk>/assign/', views.assign_team, name='assign_team'),
    path('crisis/<int:crisis_pk>/status/', views.post_status_update, name='post_status_update'),
]
