from Practica3 import funcionesBD

from tkinter import Toplevel

from tkinter import Label
from tkinter import Entry

from tkinter import LEFT
from tkinter import BOTH

from tkinter import END

from tkinter import FLAT

from tkinter import StringVar

from tkinter import Message

from Practica3 import funcionesTkinter


def list_bd():
    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor = conn.execute("""SELECT * FROM FORO """)
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
    
    conn.close()
       
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
def popularesBD():
    
    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY VISITAS DESC LIMIT 5""") 
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END, "Respuestas: "+ str(row[5]))
        lb.insert(END, "Visitas: "+ str(row[6]))
        lb.insert(END,'')
        
    
    conn.close()
   
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)
    
    
def activosBD():
    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY RESPUESTAS DESC LIMIT 10 """)
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END, "Respuestas: "+ str(row[5]))
        lb.insert(END, "Visitas: "+ str(row[6]))
        lb.insert(END,'')
   
    conn.close()
   
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
    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE TITULO LIKE '%"+text+"%'")
    
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
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
    lb=Label(v,text="Introduzca el autor")
    lb.pack(side=LEFT)
    en= Entry(v)
    en.bind("<Return>",buscarAutor)
    en.pack()  
    
def encontrarAutor(text):
    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE AUTOR LIKE '%"+text+"%'") 
    
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
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
    
    lb=Label(v,text="Introduzca el anyo (yyyy)")
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

    conn= funcionesBD.sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE FECHA LIKE '%"+text+"%' ")  
    
    ventana = funcionesTkinter.ventanaResultados(200,150,200,150)
    lb = ventana[0]
    sc = ventana[1]
    
    for row in cursor:
        lb.insert(END, "Titulo :" + row[1])
        lb.insert(END, "Autor: "+ row[2])
        lb.insert(END, "Fecha: "+ row[3])
        lb.insert(END,'')
     
    conn.close()
             
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command= lb.yview)    

        
    
    