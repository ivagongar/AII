# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import datetime
import re
from app.models import Game, Genre

def cargarSwitch(url): 
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    return soup


def extraerTitulo(soup):
    return str(soup.span.string)

def extraerGeneros(soup):
    generos = []
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



#Contemplar numero de paginas variable
def almacenarSwitch(numPages = 3):
    #fbd.crearBD()
    
    for p in range(1,numPages+1):#Cambiar luego a 64
        soup=cargarSwitch("https://www.nintendo.es/Buscar/Buscar-299117.html?f=147394-5-81&p="+str(p))
        
        
        
        pagina = soup.find_all("li", class_="searchresult_row page-list-group-item col-xs-12")
        
        for juego in pagina[2:len(pagina)]:
            
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
            game = Game.objects.get_or_create(title = titulo, defaults={'description': desc, 'type': 'Nintendo Switch', 'rating': None, 'cost': precios[0], 'on_sale_cost': precios[1],'plus_cost': None, 'start_date_on_sale': None, 'end_date_on_sale': finOferta, 'release_date': lanz})[0]
            game.save()
            
            for gen in generos:
                g = Genre.objects.get_or_create(name=gen)[0]
                g.save()
                game.genres.add(g)
            
  
        
        #for i in array:
            #titulo= extraerTitulo(i)
            #autor= extraerAutor(i)
            #fecha= extraerFecha(i)
            #enlace= "https://foros.derecho.com/"+ extraerEnlace(i)
            #respuestas= extraerRespuestas(i)
            #visitas= extraerVisitas(i)
            
            #fbd.insertRow(titulo, autor, fecha, enlace, respuestas.replace(',',''), visitas.replace(',',''))
            #print(titulo)
       
    #numRows= fbd.getNumRows()
    #messagebox.showinfo("Base de datos", "La base de datos ha sido creada perfectamente. \n Contiene "+ numRows + " registros.")


