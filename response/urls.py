from django.urls import path
from . import views

urlpatterns = [
    path('crisis/<int:pk>/assign/', views.assign_team, name='assign_team'),
    path('crisis/<int:pk>/status/', views.post_status_update, name='post_status_update'),
]
