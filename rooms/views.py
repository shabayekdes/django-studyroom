from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from .forms import RoomForm
from .models import Room
from topics.models import Topic
from chat_messages.forms import MessageForm
from chat_messages.models import Message

# Create your views here.
def list_rooms(request):
    query = request.GET.get('q')
    if query is None or query == "ALL":
        rooms = Room.objects.all()
        messages = Message.objects.all()
    else:
        messages = Message.objects.filter(Q(room__topic__name__icontains=query))
        rooms = Room.objects.search(query=query)

    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'rooms_count': rooms.count(),
        'topics': topics,
        'messages': messages,
    }
    return render(request, 'rooms/list.html', context)

def view_room(request, id=None):
    room = get_object_or_404(Room, pk=id)
    messages = room.message_set.all()
    participants = room.participants.all()

    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.user = request.user
        message.room = room
        message.save()
        room.participants.add(request.user)
        return redirect('view-room', id=id)

    context = {
        'room': room,
        'messages': messages,
        'message_form': form,
        'participants': participants,
    }
    return render(request, 'rooms/details.html', context=context)

@login_required(login_url='/login/')
def create_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.host = request.user
        obj.save()
        return redirect('list-rooms')
    context = {
        'form': form,
    }
    return render(request, 'rooms/create.html', context=context)

@login_required(login_url='/login/')
def update_room(request, id=None):
    obj = get_object_or_404(Room, pk=id)
    if request.user != obj.host:
        return HttpResponse('You are not allowed to update this room.')

    form = RoomForm(instance=obj, data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list-rooms')
    context = {
        'form': form,
        'object': obj,
    }
    return render(request, 'rooms/update.html', context=context)

@login_required(login_url='/login/')
def delete_room(request, id=None):
    obj = get_object_or_404(Room, pk=id)
    if request.user != obj.host:
        return HttpResponse('You are not allowed to delete this room.')

    if request.method == 'POST' and obj:
        obj.delete()
        return redirect('list-rooms')
    context = {
        'object': obj,
    }
    return render(request, 'rooms/delete.html', context=context)
