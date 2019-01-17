#encoding: utf-8

import urllib.request
from bs4 import BeautifulSoup
import sqlite3

from tkinter import *
from tkinter import messagebox
from Tools.demo.sortvisu import WIDTH




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
    
def popularesBD():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY VISITAS DESC LIMIT 5""")
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END, "Respuestas: "+ str(row[5]))
        lb.insert(END, "Visitas: "+ str(row[6]))
        lb.insert(END,'')
          
    
    
   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
def activosBD():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY RESPUESTAS DESC LIMIT 10 """)
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END, "Respuestas: "+ str(row[5]))
        lb.insert(END, "Visitas: "+ str(row[6]))
        lb.insert(END,'')
          
    
    
   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)

def buscar_BD_Titulo():   
    def buscarTitulo(event):
        s=en.get()
        encontrarTitulo(str(s))
        v.destroy()
        
    v= Toplevel()
    lb=Label(v,text="Introduzca el tema")
    lb.pack(side=LEFT)
    en= Entry(v)
    en.bind("<Return>",buscarTitulo)
    en.pack()
    
        
    
    
def encontrarTitulo(text):
    
    
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE TITULO LIKE '%"+text+"%'")
    
    
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
          
    
    
    conn.close()   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
    
def buscar_BD_Autor():   
    def buscarAutor(event):
        s=en.get()
        encontrarAutor(str(s))
        v.destroy()
        
    v= Toplevel()
    lb=Label(v,text="Introduzca el tema")
    lb.pack(side=LEFT)
    en= Entry(v)
    en.bind("<Return>",buscarAutor)
    en.pack()
    
        
    
    
def encontrarAutor(text):
    
    
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE AUTOR LIKE '%"+text+"%'")
    
    
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
          
    
    
    conn.close()   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
    
    
def buscar_BD_Fecha(error=False):   
    def buscarFecha(event):
       
        diaS=dia.get()
        mesS=mes.get()
        anhoS=anho.get()
        
        
        
        if(len(diaS.strip())==0 or len(mesS.strip())==0 or len(anhoS.strip())==0 ):
            v.destroy()
            buscar_BD_Fecha(True)
        else:
            v.destroy()
            encontrarFecha(diaS+"/"+mesS+"/"+anhoS)
        
    
       
        
        
    v= Toplevel()
    lb=Label(v,text="Introduzca el dia (dd)")
    lb.grid(row=0,column=0)
    dia= Entry(v, width=2)
    dia.bind("<Return>",buscarFecha)
    dia.grid(row=0,column=1)
    
    lb=Label(v,text="Introduzca el mes (MM)")
    lb.grid(row=1,column=0)
    mes= Entry(v, width=2)
    mes.bind("<Return>",buscarFecha)
    mes.grid(row=1,column=1)
    
    lb=Label(v,text="Introduzca el año (yyyy)")
    lb.grid(row=2,column=0)
    anho= Entry(v,width=4)
    anho.bind("<Return>",buscarFecha)
    anho.grid(row=2,column=1)
    
    if(error):
        var= StringVar()
        label= Message(v, textvariable=var, relief=FLAT, fg='red')
        var.set("Rellena los campos perro")
        label.grid(row=3,column=0)
        
        
    
    
    
        
    
    
def encontrarFecha(text):
    
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE FECHA LIKE '%"+text+"%' ")
    
    
    tp=Toplevel(height=200,width=150)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=200, height=150, yscrollcommand=sc.set)
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
          
    
    
    conn.close()   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)    




def mainMetodo():
    crearBD()
    
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
            
            insertRow(titulo, autor, fecha, enlace, respuestas.replace(',',''), visitas.replace(',',''))
     
     
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
       
    cursor=conn.execute("SELECT COUNT(*) FROM FORO")
    messagebox.showinfo("Base de datos", "La base de datos ha sido creada perfectamente. \n Contiene "+str(cursor.fetchone()[0]) + " registros.")

    conn.close()
        
    
def ventana():
    root=Tk()
    w= Frame(root)
    w.pack()
    
    bottomframe= Frame(root)
    bottomframe.pack(side=BOTTOM)
    
    mb1=Menubutton(bottomframe, text="Datos", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Almacenar",command=mainMetodo)
    mb1.menu.add_command(label="Listar",command=list_bd)
    mb1.menu.add_command(label="Salir",command=root.destroy)

    mb1.grid(row=0,column=0)
    
    mb1=Menubutton(bottomframe, text="Buscar", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Tema",command=buscar_BD_Titulo)
    mb1.menu.add_command(label="Autor",command=buscar_BD_Autor)
    mb1.menu.add_command(label="Fecha",command=buscar_BD_Fecha)
   

    mb1.grid(row=0,column=1)
    
    
    mb1=Menubutton(bottomframe, text="Estadisticas", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Temas más populares",command=popularesBD)
    mb1.menu.add_command(label="Temas más activos",command=activosBD)
   

    mb1.grid(row=0,column=2)
    
    #DESC
    
    root.mainloop()
    
ventana()
        
    

    


