from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('populateSwitch', views.populateSwitch, name='populateSwitch'),
    path('listAll', views.mostrarJuegos, name='listAll'),
    path('signUp', views.signUp, name='signUp'),
    path('logIn', views.logIn, name='signUp'),
    path('logOut', views.logOut, name='logOut'),
    path('editLibrary', views.editLibrary, name='editLibrary'),
    path('listLibrary', views.listLibrary, name='listLibrary'),
    path('deleteLibrary', views.deleteLibrary, name='deleteLibrary'),
    path('viewLibrary', views.viewLibrary, name='viewLibrary'),
    path('addGame', views.addGame, name='addGame'),
    path('removeGame', views.removeGame, name='removeGame'),
    path('populatePSN', views.populatePSN, name="populatePSN"),
]
