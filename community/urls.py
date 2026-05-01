from django.urls import path
from . import views

urlpatterns = [
    path('crisis/<int:crisis_pk>/volunteer/', views.volunteer_signup, name='volunteer_signup'),
    path('crisis/<int:crisis_pk>/donate/', views.donate, name='donate'),
]