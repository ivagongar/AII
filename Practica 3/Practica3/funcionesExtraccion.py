import urllib.request
from bs4 import BeautifulSoup
from Practica3 import funcionesBD as fbd
from tkinter import messagebox


def cargar_web(url):    
    response = urllib.request.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
        
    return soup

def extraerTitulo(soup):
    return soup.div.div.h3.a['title']

def extraerAutor(soup):
    return soup.div.span.a.string

def extraerFecha(soup):
    text= soup.div.span.a['title'].split(',')[1].strip()
    return text[2:len(text)].strip()

def extraerEnlace(soup):
    return soup.div.div.h3.a['href']

def extraerRespuestas(soup):
    return soup.ul.li.a.string

def extraerVisitas(soup):
    text= soup.ul.li.next_sibling.next_sibling.string.split(':')[1]
    return text.strip()

#Contemplar numero de paginas variable
def almacenarBD():
    fbd.crearBD()
    
    for p in range(1,4):
        soup=cargar_web("https://foros.derecho.com/foro/20-Derecho-Civil-General/page"+str(p))
        
        
        array= soup.find_all("div", class_="nonsticky")
        
        for i in array:
            titulo= extraerTitulo(i)
            autor= extraerAutor(i)
            fecha= extraerFecha(i)
            enlace= "https://foros.derecho.com/"+ extraerEnlace(i)
            respuestas= extraerRespuestas(i)
            visitas= extraerVisitas(i)
            
            fbd.insertRow(titulo, autor, fecha, enlace, respuestas.replace(',',''), visitas.replace(',',''))
     
       
    cursor= fbd.getNumRows()
    messagebox.showinfo("Base de datos", "La base de datos ha sido creada perfectamente. \n Contiene "+str(cursor.fetchone()[0]) + " registros.")

