from gettext import install
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rooms.models import Room
from chat_messages.models import Message
from topics.models import Topic
from .forms import ProfileUpdateForm

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
            return redirect('home')
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
        return redirect('home')
    context = {"form": form}
    return render(request, "accounts/register.html", context)

@login_required
def show_profile(request, id=None):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    messages = Message.objects.all()
    
    context = {
        'user': user,
        'topics': topics,
        'rooms': rooms,
        'messages': messages,
    }
    return render(request, "accounts/profile.html", context=context)

@login_required
def update_profile(request, id=None):
    user = request.user
    form = ProfileUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        user_obj = form.save()
        return redirect('show-profile', id=user_obj.id)
    context = {"form": form}
    return render(request, "accounts/update_profile.html", context=context)
