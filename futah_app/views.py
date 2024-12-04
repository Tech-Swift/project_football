from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from futah_app.models import Player


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})

def dashboard(request):
    if request.user.is_authenticated:
        players = Player.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {"players": players})
    return redirect('home')
