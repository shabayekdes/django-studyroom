from django.urls import path

from .views import (
    list_rooms,
    create_room
)

urlpatterns = [
    path('', list_rooms, name='list-rooms'),
    path('create/', create_room, name='create-room'),
]
