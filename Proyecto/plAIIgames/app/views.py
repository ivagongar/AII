from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from app.models import Genre, Game, Library
from app.forms import LibraryForm
from app import funciones
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, 'app/index.html')


def logOut(request):
    try:
        logout(request)
    except:
        pass

    return render(request, 'app/index.html')


def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        amove = User.objects.get(username=username)

        user = authenticate(username=username, password=raw_password)
        if not user:
            return render(request, 'app/index.html', {'loginerror': 'error al logear'})

        login(request, user)
        return redirect('index')
    else:
        return render(request, 'app/index.html')


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
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'app/signUp.html', {'form': form})


def editLibrary(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('listLibrary')

    form = LibraryForm(initial={'user': request.user})

    return render(request, 'app/editLibrary.html', {'form': form})

def listLibrary(request):
    return render(request, 'app/listLibrary.html')

def deleteLibrary(request):
    Library.objects.get(id=request.GET['library']).delete()

    return redirect('listLibrary')


