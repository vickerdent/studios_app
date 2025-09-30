from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messages/', views.messages, name='messages'),
    path('messages/<uuid:message_id>/', views.message_details, name='message_details'),
    path('messages/<uuid:message_id>/add_comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_messages, name='search_messages'),
    path('conferences/', views.conferences, name='conferences'),
    path('conferences/<int:conference_id>/', views.conference_details, name='conference_details'),
    path('about/', views.about, name='about'),
    path('notifications/register/', views.register_notifications, name='register_notifications'),
    path('sw.js', views.service_worker, name='service_worker'),
]
