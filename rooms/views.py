from django.shortcuts import render, redirect

from .forms import RoomForm

# Create your views here.
def create_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(request, 'rooms/list.html', {'form': form})
    context = {
        'form': form,
    }
    return render(request, 'rooms/create.html', context=context)
