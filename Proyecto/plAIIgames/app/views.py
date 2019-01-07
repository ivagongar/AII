from django.shortcuts import render
from app.models import Genre, Game
from app import funciones

# Create your views here.

def index(request):
    return render(request,'app/index.html')

def populateSwitch(request):
    funciones.almacenarSwitch(3)
    
    return render(request,'app/index.html')

def mostrarJuegos(request):
    juegos = Game.objects.all()
    
    return render(request,'app/listAll.html',{"games":juegos})