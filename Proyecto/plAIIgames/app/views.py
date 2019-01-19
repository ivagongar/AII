from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from app.models import Genre, Game, Library
from app.forms import LibraryForm
from app import funciones
from django.contrib.auth.models import User
from django.template.context_processors import request


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

def populatePSN(request):
    funciones.almacenarPSN(3)
    
    return render(request, 'app/index.html')

def mostrarJuegos(request):
    juegos = Game.objects.all()

    return render(request, 'app/listAll.html', {"games": juegos})

def mostrar_PSgames(request):
    juegos = Game.objects.all().filter(type="PS")
    return render(request, 'app/PSgames.html')

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


def addGame(request):
    if request.method == 'POST':
        num = request.POST['libreria']
        libreria = Library.objects.get(id=int(num))

        for g in request.POST['games']:
            game = Game.objects.get(id=g)
            libreria.games.add(game)
        libreria.save()

    else:
        libreria = Library.objects.get(id=request.GET['library'])

        juegos = Game.objects.all()
        games = list()
        for j in juegos:
            games.append(j)
        for g in libreria.games.all():
            games.remove(g)

        return render(request, 'app/addGame.html', {'libreria': libreria, 'games': games})

    return redirect('listLibrary')


def removeGame(request):
    if request.method == 'POST':
        num = request.POST['libreria']
        libreria = Library.objects.get(id=int(num))

        for g in request.POST['games']:
            game = Game.objects.get(id=g)
            libreria.games.remove(game)
        libreria.save()

    else:
        libreria = Library.objects.get(id=request.GET['library'])

        games = libreria.games.all()

        return render(request, 'app/removeGame.html', {'libreria': libreria, 'games': games})

    return redirect('listLibrary')


def viewLibrary(request):
    return render(request, 'app/viewLibrary.html', {'library': Library.objects.get(id=request.GET['library'])})
