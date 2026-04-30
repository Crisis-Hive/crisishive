from django.urls import path
from . import views

urlpatterns = [
    path('', views.crisis_feed, name='crisis_feed'),
    path('crisis/<int:pk>/', views.crisis_detail, name='crisis_detail'),
    path('crisis/report/', views.report_crisis, name='report_crisis'),
    path('crisis/<int:pk>/upvote/', views.toggle_upvote, name='toggle_upvote'),
]