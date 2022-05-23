from django.shortcuts import render, redirect, get_object_or_404

from .forms import RoomForm
from .models import Room

# Create your views here.
def list_rooms(request):
    obj = Room.objects.all()
    context = {
        'objects': obj
    }
    return render(request, 'rooms/list.html', context)

def create_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list-rooms')
    context = {
        'form': form,
    }
    return render(request, 'rooms/create.html', context=context)

def update_room(request, id=None):
    obj = get_object_or_404(Room, pk=id)
    form = RoomForm(instance=obj, data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list-rooms')
    context = {
        'form': form,
        'object': obj,
    }
    return render(request, 'rooms/update.html', context=context)
