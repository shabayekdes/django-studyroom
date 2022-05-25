from django.urls import path

from .views import (
    list_rooms,
    view_room,
    create_room,
    update_room
)

urlpatterns = [
    path('', list_rooms, name='list-rooms'),
    path('create/', create_room, name='create-room'),
    path('<int:id>/', view_room, name='view-room'),
    path('<int:id>/edit/', update_room, name='update-room'),
]
