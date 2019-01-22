# -*- coding: utf-8 -*-
import shelve, os
from app.models import Game, Library
from django.contrib.auth.models import User
   
def loadDict():
    shelf = shelve.open(os.path.join(os.getcwd(),"sim_matrix.dat"))
    shelf['SimItems']=matrizItems()
    shelf.close()    
    
def getMatriz():    
    shelf = shelve.open(os.path.join(os.getcwd(),"sim_matrix.dat"))
    matrizItems = shelf['SimItems']
    shelf.close()
    return matrizItems
    
def matrizItems():    
    sim_items= {}
    
    # Iteramos sobre todos los campeones para calcular sus campeones similares
    for g1 in Game.objects.all():
        for g2 in Game.objects.all():
            if (g1.id == g2.id):
                continue
            
            sim = 0
            
            # Generos: 3 puntos por cada genero en comun
            sim += len(set(g1.genres.all()).intersection(g2.genres.all()))*3
            
            # Precio : 2 puntos si la diferencia es 5 o menos, 1 punto si es de 10 o menos
            if(g1.on_sale_cost is not None and g2.on_sale_cost is not None):
                dif = abs(g1.on_sale_cost - g2.on_sale_cost)
            
                if dif <= 10:
                    sim += 1
                    
                if dif <= 5:
                    sim += 1
            
            # = Rating: Bonus para rating alto, 0.25 puntos por la puntuacion
            if g2.rating:
                sim += 0.25*g2.rating
            
            # = Release date: Bonus si ha salido de 0.5 puntos
            if g2.release_date:
                sim += 0.5
            
            # = Oferta: Bonus si esta rebajado de 0.1 puntos por euro de descuento
            if g2.cost:
                sim += 0.1*(g2.cost - g2.on_sale_cost)
            
            sim_items.setdefault(int(g1.id), [])
            sim_items[int(g1.id)].append([int(g2.id),sim])
                
    return sim_items


def getRecommendation(userFavs, matrizItems):
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (g1, num) in userFavs.items():
        # Loop over items similar to this one
        for (g2, similarity) in matrizItems[g1.id]:
            # Ignore if this user has already rated this item
            if g2 in userFavs: continue
            # Weighted sum of rating times similarity
            scores.setdefault(g2, 0)
            scores[g2] += similarity * num
            # Sum of all the similarities
            totalSim.setdefault(g2, 0)
            totalSim[g2] += similarity

    # Divide each total score by total weighting to get an average
    try:
        rankings = [(score / (totalSim[game]+1), game) for game, score in scores.items()]
    except ZeroDivisionError:
        rankings = []

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


def userFavs(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    libraries = Library.objects.filter(user=user)
    
    userFavs = {}
    
    for lib in libraries:
        for game in lib.games.all():
            userFavs.setdefault(game, 0)
            userFavs[game] += 1
    
    return userFavs

