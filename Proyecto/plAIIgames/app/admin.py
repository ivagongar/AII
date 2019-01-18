from django.contrib import admin

# Register your models here.
from app.models import Game, Library, OfferCategory, Genre

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Library)
admin.site.register(OfferCategory)
