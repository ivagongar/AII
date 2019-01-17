#encoding: utf-8
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime 
from .models import Game, Genre

def cargar_web(url):
    
    response = urllib.request.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def cargar_web_selenium(url):
    
    #SELENIUM 
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    
    return soup

def extraerHref(soup):
    return soup.a['href']

def extraerTitle(soup):
    return soup.h2.string
def extraerDescription(soup):
    description = soup.find("p", style = "direction:ltr").next_element
    if(str(description).startswith("El precio de oferta especial")):
        description = description.next_element.next_element.next_element
    if(str(description).startswith("El precio de oferta especial")):
        description = description.next_element.next_element.next_element.next_element
    return description

def extraerCost(soup):
    return soup.find("div","sku-info").div.div.h3.string.replace("€","").strip()

def extraerOldSaleCost(soup):
    return soup.find("div","sku-info").div.find("div","price").string.replace("€","").strip()
       
def extraerPlusCost(soup): 
    if(soup.div.find("div", "price-display__price--is-plus-upsell") is not None):
        return soup.div.find("div", "price-display__price--is-plus-upsell").string.replace("€","").strip()
    
def extraerStartDateOnSale(soup):    
    if(soup.find("div", "price-availability") != None):
        fecha = soup.find("div", "price-availability").string.strip().replace("Este precio solo es válido del ","").split('al ')[0].strip()
        return datetime.strptime(fecha, '%d/%m/%Y %I:%M %p')
    
 
def extraerEndDateOnSale(soup):
    if(soup.find("div", "price-availability") != None):
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
    fecha =  soup.div.span.next_sibling.next_sibling.string.replace("Lanzado ","").strip().replace("Ene","Jan").replace("Dic","Dec").replace("Abr", "Apr").replace("Ago","Aug")
    return datetime.strptime(fecha, "%d %b %Y") 

def extraerGenre(soup):  
    return soup.find("div","tech-specs").find("div","tech-specs__pivot-menus").ul.find_all("li")
    
      
def almacenarBD(pag):
    dicc = dict()
    count = 0
    for p in range(1,pag):       
        soup = cargar_web("https://store.playstation.com/es-es/grid/STORE-MSF75508-JANSALE19PS4/"+str(p)+"?gameContentType=games")    
        array = soup.find_all("div", class_="grid-cell-row__container")
        for i in array:
            href = extraerHref(i)
            print(href)
            s = count
            dicc[s] = "https://store.playstation.com"+href
            print(dicc[s])
            count=count+1      

    for value in dicc.values():
        print("PROCEDE A ENTRAR EN EL JUEGO")
        game = cargar_web_selenium(value)
        array2 = game.find_all("div", class_="large-9 columns pdp__right-content")
        for i in array2: 
            titulo = extraerTitle(i)
            desc = extraerDescription(i)
            startDateOnSale = extraerStartDateOnSale(i)
            endDateOnSale =extraerEndDateOnSale(i)
            releaseDate = extraerReleaseDate(i)
            rate = extraerRating(i)
        array3 = game.find_all("div", class_="large-3 columns pdp__left-content")
        for j in array3:
            costNow = extraerCost(j)
            oldCost = extraerOldSaleCost(j)
            costPlus = extraerPlusCost(j)
            generos = extraerGenre(j)
            generosCorrectos =[]
            for gen in generos:
                g = Genre.objects.get_or_create(name=gen)[0]
                g2 = g.save()
                generosCorrectos.append(g2)
        
        game = Game.objects.get_or_create(title = titulo, description=desc, type="PS",
                 rating=rate, cost=oldCost, on_sale_cost=costNow, plus_cost=costPlus, 
                 start_date_on_sale=startDateOnSale, end_date_on_sale=endDateOnSale, 
                 release_date=releaseDate, genre=generosCorrectos)
        game.save()
