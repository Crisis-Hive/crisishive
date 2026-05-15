from django.urls import path
from . import views

urlpatterns = [
    path('', views.crisis_feed, name='crisis_feed'),
    path('crisis/report/', views.report_crisis, name='report_crisis'),
    path('crisis/my-reports/', views.my_reports, name='my_reports'),
    path('crisis/<int:pk>/', views.crisis_detail, name='crisis_detail'),
    path('crisis/<int:pk>/edit/', views.edit_crisis, name='edit_crisis'),
    path('crisis/<int:pk>/delete/', views.delete_crisis, name='delete_crisis'),
    path('crisis/<int:pk>/upvote/', views.toggle_upvote, name='toggle_upvote'),
    path('media/<int:media_pk>/delete/', views.delete_media, name='delete_media'),
]