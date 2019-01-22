# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import re
from app.models import Game, Genre, OfferCategory
import urllib.request

from datetime import datetime 

def cargarSwitch(url): 
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    return soup


def cargar_web(url):
    
    response = urllib.request.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def cargar_web_selenium(url):
    
    #SELENIUM 
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    
    return soup

def extraerTitulo(soup):
    return str(soup.span.string)

def extraerGeneros(soup):
    generos = []
    if (soup.find("span", class_="hidden-xs hidden-sm").span) is not None:
        bruto = str(soup.find("span", class_="hidden-xs hidden-sm").span.find_all("span", recursive=False))
        res = bruto.replace("<span>", "").replace("</span>", "").replace("[", "").replace("]", "").replace("<!-- -->", "").split(",")
        for r in res:
            if r.strip():
                generos.append(r)
    
    return generos

def extraerDescripcion(soup):
    return str(soup.find("p",class_="hidden-xs visible-sm visible-md visible-lg").string)


#data-price-box-price="enddate"

def extraerPrecios(soup):
    res = [None,None] #[Original, descuento]
    pre = soup.find("p", class_="page-data-purchase")

    if pre is None:#No hay precio
        return res
    else:
        sec = pre.find("span",class_="original-price")
        #[0:len(precioString)-2]
        if sec is None:#Hay un precio único
            precioString = str(pre.span.string)
            precio = float(precioString.replace(",", ".").replace("€*", "").strip())
            res[0] = precio
        else:#Hay dos precios
            res[0] = float(str(sec.string).replace(",", ".").replace("€", "").strip())
            desc = pre.find("span",class_="discount")
            res[1] = float(str(desc.string).replace(",", ".").replace("€*", "").strip())
        
        return res
    
def extraerFinOferta(soup):
    link = "https://www.nintendo.es" + str(soup.div.div.a['href'])
    
    soup2 = cargarSwitch(link)
    raw = str(soup2.find("div", class_="row price-box-item discount").p.next_sibling.next_sibling.next_sibling.next_sibling.string)
    fechaString = raw[len(raw)-10:len(raw)].split("-")
    year = fechaString[2]
    month = fechaString[1]
    day = fechaString[0]
    
    return datetime.datetime(int(year),int(month),int(day),23,59)
    
    
    #return link

def extraerLanzamiento(soup):
    raw = soup.find("p",class_="page-data").text
    sec = raw.replace("Nintendo Switch","").replace(u'\u2022',"").strip().split(" ")[0]
    
    pattern = re.compile("^\d+-\d+-\d+$")
    if not pattern.match(sec):
        res = None
    else:
        fechaString = sec.split("-")
        year = fechaString[2]
        month = fechaString[1]
        day = fechaString[0]
        
        res = datetime.datetime(int(year),int(month),int(day),0,0)
    
    return res
def extraerFoto(soup):
    return soup.img['src']


#Contemplar numero de paginas variable
def almacenarSwitch(numPages = 3):
    #fbd.crearBD()
    
    for p in range(1,numPages+1):#Cambiar luego a 64
        soup=cargarSwitch("https://www.nintendo.es/Buscar/Buscar-299117.html?f=147394-5-81&p="+str(p))  
        pagina = soup.find_all("li", class_="searchresult_row page-list-group-item col-xs-12")
        
        for juego in pagina[2:len(pagina)]:
            foto = extraerFoto(juego)
            generos = extraerGeneros(juego)
            titulo = extraerTitulo(juego)
            desc = extraerDescripcion(juego)
            precios = extraerPrecios(juego)
            finOferta = None
            if precios[1] is not None:
                try:
                    finOferta = extraerFinOferta(juego)
                except:
                    finOferta = None
            
            lanz = extraerLanzamiento(soup)
            
            
             
            #game = Game.objects.get_or_create(title = titulo, defaults={'description': desc, 'type': 'Nintendo Switch', 'rating': None, 'cost': precios[0], 'on_sale_cost': precios[1],'plus_cost': None, 'start_date_on_sale': None, 'end_date_on_sale': finOferta, 'release_date': lanz, 'genres': generosBien, 'offer_categories': []})
            game = Game.objects.get_or_create(title = titulo, type="Nintendo Switch", defaults={'description': desc, 'photo' : foto, 'rating': None, 'cost': precios[1], 'on_sale_cost': precios[0],'plus_cost': None, 'start_date_on_sale': None, 'end_date_on_sale': finOferta, 'release_date': lanz})[0]
            game.save()
            
            for gen in generos:
                g = Genre.objects.get_or_create(name=gen)[0]
                g.save()
                game.genres.add(g)
                 
      
def extraerHref(soup):
    return soup.a['href']

def extraerPhoto(soup):
    return soup.find("div", class_="product-image__img product-image__img--main").img['src']

def extraerHrefOfertas(soup):
    return soup.a['href'].replace("?emcid=pa-st-165916","")

def extraerOfferCat(soup):
    return soup.a.span.string

def extraerTitle(soup):
    return soup.h2.string

def extraerDescription(soup):
    description = soup.find("p", style = "direction:ltr").next_element
    if(str(description.string).startswith("RESERVA")):
        description = description.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
    if(str(description).startswith("El precio de oferta especial")):
        description = description.next_element.next_element.next_element
    if(str(description).startswith("El precio de oferta especial")):
        description = description.next_element.next_element.next_element.next_element
    return description

def extraerCost(soup):
    return soup.find("div","sku-info").div.div.h3.string.replace("€","").replace(",",".").strip()

def extraerOldSaleCost(soup):
    oldCost = 0
    if soup.find("div","sku-info").div.find("div","price") is not None:
        oldCost = soup.find("div","sku-info").div.find("div","price").string.replace("€","").replace(",",".").strip()
    return oldCost

def extraerType(soup):
    tipo = "Unkwown"
    if soup.find("div","sku-info").find("div","playable-on__button-set"):
        tipo = soup.find("div","sku-info").find("div","playable-on__button-set").a.string
    return tipo
       
def extraerPlusCost(soup): 
    if soup.div.find("div", "price-display__price--is-plus-upsell") is not None:
        return soup.div.find("div", "price-display__price--is-plus-upsell").string.replace("€","").replace(",",".").strip()
    
def extraerStartDateOnSale(soup):    
    if soup.find("div", "price-availability") is not None:
        fecha = soup.find("div", "price-availability").string.strip().replace("Este precio solo es válido del ","").split('al ')[0].strip()
        return datetime.strptime(fecha, '%d/%m/%Y %I:%M %p')
    
 
def extraerEndDateOnSale(soup):
    if  soup.find("div", "price-availability") is not None:
        fecha = soup.find("div", "price-availability").string.strip().replace("Este precio solo es válido del ","").strip().split('al ')[1].replace(".","").strip()
        return datetime.strptime(fecha, '%d/%m/%Y %I:%M %p')
    
def extraerRating(soup):
    rating = 0
    completas = soup.find("div", "star-rating")
    if(completas is not None):
        completas = completas.findAll("i", "star-rating__star fa fa-star ember-view")
        for i in completas:
            rating = rating+1
        
        medias = soup.find("div", "star-rating").findAll("i", "star-rating__star fa fa-star-half-o ember-view")
        for i in medias:
            rating = rating+0.5
    
    return rating
    
def extraerReleaseDate(soup): 
    if soup.div.span.next_sibling.next_sibling is not None:
        fecha =  soup.div.span.next_sibling.next_sibling.string.replace("Lanzado ","").strip().replace("Ene","Jan").replace("Dic","Dec").replace("Abr", "Apr").replace("Ago","Aug")
        return datetime.strptime(fecha, "%d %b %Y") 

def extraerGenre(soup):  
    result = []
    if soup.find("div","tech-specs").find("div","tech-specs__pivot-menus").ul is not None:  
        genres = soup.find("div","tech-specs").find("div","tech-specs__pivot-menus").ul.find_all("li")
        for gen in genres:
            result.append(gen.string)
    return result
    
      
def almacenarPSN(pag):
    dicc = {} 
    dicc2 = {}
    count = 0
    for p in range(1,pag):       
        soup = cargar_web("https://store.playstation.com/es-es/grid/STORE-MSF75508-FULLGAMES/"+str(p)+"?gameContentType=games")    
        array = soup.find_all("div", class_="grid-cell grid-cell--game")
        for i in array:
            href = extraerHref(i)
            s = count
            dicc[s] = "https://store.playstation.com"+href
            dicc2["https://store.playstation.com"+href] = extraerPhoto(i)
            count=count+1      
    for value in dicc.values():
        game = cargar_web_selenium(value)
        array2 = game.find_all("div", class_="large-9 columns pdp__right-content")
        for i in array2: 
            titulo = extraerTitle(i)
            desc = extraerDescription(i)
            startDateOnSale = extraerStartDateOnSale(i)
            endDateOnSale =extraerEndDateOnSale(i)
            releaseDate = extraerReleaseDate(i)
            rate = extraerRating(i)
            foto = dicc2[value]
        array3 = game.find_all("div", class_="large-3 columns pdp__left-content")
        for j in array3:
            costNow = extraerCost(j)
            oldCost = extraerOldSaleCost(j)
            costPlus = extraerPlusCost(j)
            generos = extraerGenre(j)            
            tipo = extraerType(j)
            
        game = Game.objects.get_or_create(title = titulo,
                description=desc,
                type=tipo,
                rating=rate,
                cost=oldCost,
                on_sale_cost=costNow,
                plus_cost=costPlus, 
                start_date_on_sale=startDateOnSale,
                end_date_on_sale=endDateOnSale,
                release_date=releaseDate, 
                photo = foto
                )[0]        
        game.save()      
        for gen in generos:
            g = Genre.objects.get_or_create(name=gen)[0]
            g.save()
            game.genres.add(g)
          

def cargaOfertas():
    soupOffers = cargar_web_selenium("https://store.playstation.com/es-es/grid/STORE-MSF75508-GAMESPECIALOFF/1?emcid=pa-st-165916")
    array = soupOffers.find_all("div", class_="grid-cell__body")
    print(array)
    dicc = dict()
    count = 0
    for i in array:
        s = count
        href = extraerHrefOfertas(i)
        m = "https://store.playstation.com"+href+"/"
        for p in range(1, 11):
            dicc[s] = m+str(p)+"?emcid=pa-st-165916"
            s = s+1
        count = count+100
            
    print(dicc)
    for value in dicc.values():
        page = cargar_web_selenium(value)
        offer = page.find("h3", class_="grid-header__title").string
        gamesContained = page.find_all("div", class_="grid-cell grid-cell--game")
        for g in gamesContained:
            tipo = g.find("div","grid-cell__left-detail grid-cell__left-detail--detail-1").string
            nombre = g.find("div", class_="grid-cell__title").span.string
            tamanio = len(Game.objects.filter(title=nombre, type=tipo))
            if tamanio !=0:
                game = Game.objects.filter(title=nombre, type=tipo)[0]
                offerCat = OfferCategory.objects.get_or_create(name=offer)[0]
                offerCat.save()
                game.offer_categories.add(offerCat)
