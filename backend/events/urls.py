"""
Events URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_create, name='event_list_create'),
    path('<str:event_id>/', views.event_detail, name='event_detail'),
    path('<str:event_id>/rsvp/', views.event_rsvp, name='event_rsvp'),
    path('user/my-events/', views.user_events, name='user_events'),
]
