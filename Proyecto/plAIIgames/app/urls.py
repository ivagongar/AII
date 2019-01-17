from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('populateSwitch', views.populateSwitch, name='populateSwitch'),
    path('listAll', views.mostrarJuegos, name='listAll'),
    path('signUp', views.signUp, name='signUp')

]


