from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rooms.models import Room
from chat_messages.models import Message
from topics.models import Topic

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    messages = Message.objects.all()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'rooms_count': rooms.count(),
        'topics': topics,
        'messages': messages,
    }
    return render(request, 'home.html', context=context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("list-rooms")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list-rooms')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('list-rooms')
    context = {"form": form}
    return render(request, "accounts/register.html", context)

@login_required
def show_profile(request, id=None):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()

    context = {
        'user': user,
        'rooms': rooms,
    }
    return render(request, "accounts/show_profile.html", context=context)
