from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from app.models import Genre, Game
from app import funciones


# Create your views here.

def index(request):
    try:
        auth = request.user.username
    except:
        auth = None

    return render(request, 'app/index.html', {"username": auth})


def populateSwitch(request):
    funciones.almacenarSwitch(3)

    return render(request, 'app/index.html')


def mostrarJuegos(request):
    juegos = Game.objects.all()

    return render(request, 'app/listAll.html', {"games": juegos})


def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'app/signUp.html', {'form': form})
