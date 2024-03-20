from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('chats/<slug:slug>/', views.room, name='room'),
    path('create/', views.create_room, name='create_room'),
]
