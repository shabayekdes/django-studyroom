from pydoc_data.topics import topics
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import RoomForm
from .models import Room
from topics.models import Topic

# Create your views here.
def list_rooms(request):
    query = request.GET.get('q')
    if query is None or query == "ALL":
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.search(query=query)

    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'rooms_count': rooms.count(),
        'topics': topics,
    }
    return render(request, 'rooms/list.html', context)

@login_required(login_url='/login/')
def create_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
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
