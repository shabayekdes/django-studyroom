from django.shortcuts import render, redirect

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
