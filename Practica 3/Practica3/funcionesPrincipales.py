from Practica3 import funcionesBD

from tkinter import Toplevel
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import Label
from tkinter import Entry

from tkinter import RIGHT
from tkinter import LEFT
from tkinter import BOTH

from tkinter import Y
from tkinter import END

from tkinter import FLAT

from tkinter import StringVar

from tkinter import Message

from Practica3 import funcionesTkinter


def list_bd():
    cursor=funcionesBD.selectAll()
    
    ventana = funcionesTkinter.ventanaResultados()
    lb = ventana[0]
    sc = ventana[1]
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
def popularesBD():
    cursor= funcionesBD.selectPopulares()
    
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
    cursor= funcionesBD.selectActivos()
    
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
    lb=Label(v,text="Introduzca el tema:")
    lb.pack(side=LEFT)
    en= Entry(v)
    en.bind("<Return>",buscarTitulo)
    en.pack()
       
    
def encontrarTitulo(text):
    cursor= funcionesBD.findTitulo(text)
    
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
    cursor= funcionesBD.findAutor(text)
    
    
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
    lb=Label(v,text="Introduzca el día (dd)")
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
        #Mirar si cambiar Message por Label
        label= Message(v, textvariable=var, relief=FLAT, fg='red')
        var.set("Rellena los campos perro")
        label.grid(row=3,column=0)
    
    
def encontrarFecha(text):

    cursor=funcionesBD.findFecha(text)
    
    
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

        
    
    