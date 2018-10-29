#encoding: utf-8

import urllib.request
from bs4 import BeautifulSoup
import sqlite3

from tkinter import *
from tkinter import messagebox
from Tools.demo.sortvisu import WIDTH




def cargar_web():
    response = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General")
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

def crearBD():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    conn.execute("DROP TABLE IF EXISTS FORO")
    conn.execute('''CREATE TABLE FORO(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITULO     TEXT     NOT NULL,
                AUTOR       TEXT     NOT NULL,
                FECHA      TEXT     NOT NULL,
                ENLACE     TEXT    NOT NULL,
                RESPUESTAS  INTEGER NOT NULL,
                VISITAS  INTEGER NOT NULL);''') 
      
    
    conn.close()   
    
def insertRow(titulo,autor, fecha,enlace,respuestas,visitas):
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    conn.execute("""INSERT INTO FORO(TITULO,AUTOR,FECHA,ENLACE,RESPUESTAS,VISITAS) VALUES(?,?,?,?,?,?);""",(titulo,autor,fecha,enlace,respuestas,visitas))
    conn.commit()
    
    conn.close()
    
def list_bd():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO """)
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
          
    
    
   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
    

def mainMetodo():
    
    soup=cargar_web()
    crearBD()
    
    array= soup.find_all("div", class_="nonsticky")
    
    for i in array:
        titulo= extraerTitulo(i)
        autor= extraerAutor(i)
        fecha= extraerFecha(i)
        enlace= "https://foros.derecho.com/"+ extraerEnlace(i)
        respuestas= extraerRespuestas(i)
        visitas= extraerVisitas(i)
        
        insertRow(titulo, autor, fecha, enlace, respuestas, visitas)
  
        


    
def ventana():
    root=Tk()
    
    w= Frame(root, height=90, width=90)
    w.pack()
    
    bottomframe= Frame(root)
    bottomframe.pack(side=TOP)
    
    mb=Menubutton(bottomframe, text="Datos", relief=RAISED )
    mb.grid()
    mb.menu =Menu(mb, tearoff = 0 )
    mb["menu"]=mb.menu

    mb.menu.add_command(label="Almacenar",command=mainMetodo)
    mb.menu.add_command(label="Listar",command=list_bd)

    mb.pack()
    
    root.mainloop()
    
ventana()
        
    

    


