import urllib.request
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def cargar_web(url): 
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
        
    return soup

def cargarWeb2(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'})
    soup = BeautifulSoup(response.content, "lxml")
    
    return soup

def extraerTitulo(soup):
    return str(soup.span.string)

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
def almacenarSwitch():
    #fbd.crearBD()
    
    for p in range(1,5):#Cambiar luego a 64
        soup=cargarWeb2("https://www.nintendo.es/Buscar/Buscar-299117.html?f=147394-5-81&p="+str(p))
        
        
        #array= soup.find_all("ul",class_="results")
        array = soup.find_all("ul", class_="results")
        print(array[0])
        
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

almacenarSwitch()