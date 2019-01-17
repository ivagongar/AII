from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Genre(models.Model):
    """
    Géneros de los juegos, sólo tendrán un campo 'name' que sera único para evitar que cuando leamos géneros de dos plataformas diferentes se creen más de uno igual
    """
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class OfferCategory(models.Model):
    """
    Categoría de la oferta:
    En el caso de ps si miras su store en rebajas y ofertas habrá diferentes tipos, para saber a que tipo pertenece cada uno habrá que recorrerse todos los juegos que tiene e irlos añadiendo
    """
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    """
    Juego, atributos conflictivos:
        - type: Indica la plataforma PS4,PS vita, PS3, Nintendo...
        - plus_cost: Si por estar suscrito a su plataforma como en el caso de la ps plus la rebaja es mayor
    """
    title = models.TextField(unique=True)
    description = models.TextField()
    type = models.TextField()
    rating = models.IntegerField(blank=True,null=True)
    cost = models.FloatField(blank=True,null=True)
    on_sale_cost = models.FloatField(blank=True,null=True)
    plus_cost = models.FloatField(blank=True,null=True)
    start_date_on_sale = models.DateTimeField(null=True)
    end_date_on_sale = models.DateTimeField(null=True)
    release_date = models.DateTimeField(null=True)

    genres = models.ManyToManyField(Genre, related_name='games')
    offer_categories = models.ManyToManyField(OfferCategory, related_name='games')

    def __str__(self):
        return self.title


class Library(models.Model):
    """
      Librerías para guardar tus juegos
    """
    title = models.TextField()
    description = models.TextField()

    games = models.ManyToManyField(Game, related_name='libraries')
    user = models.ForeignKey(User, related_name="library", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
