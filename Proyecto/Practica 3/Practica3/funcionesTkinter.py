from Practica3 import funcionesExtraccion as fe
from Practica3 import funcionesPrincipales as fp


from tkinter import Toplevel
from tkinter import Scrollbar
from tkinter import Listbox


from tkinter import RIGHT

from tkinter import BOTTOM


from tkinter import Y

from tkinter import RAISED


from tkinter import Tk
from tkinter import Frame
from tkinter import Menubutton
from tkinter import Menu

def ventanaResultados(tlheight,tlwidth,lbwidth,lbheight):
    tp=Toplevel(height=tlheight,width=tlwidth)
    sc= Scrollbar(tp)
    sc.pack(side=RIGHT, fill=Y)
    lb=Listbox(tp, width=lbwidth, height=lbheight, yscrollcommand=sc.set)
    
    return lb,sc

def ventanaPrincipal():
    root=Tk()
    w= Frame(root)
    w.pack()
    
    bottomframe= Frame(root)
    bottomframe.pack(side=BOTTOM)
    
    mb1=Menubutton(bottomframe, text="Datos", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Almacenar",command=fe.almacenarBD)
    mb1.menu.add_command(label="Listar",command=fp.list_bd)
    mb1.menu.add_command(label="Salir",command=root.destroy)

    mb1.grid(row=0,column=0)
    
    mb1=Menubutton(bottomframe, text="Buscar", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Tema",command=fp.buscar_BD_Titulo)
    mb1.menu.add_command(label="Autor",command=fp.buscar_BD_Autor)
    mb1.menu.add_command(label="Fecha",command=fp.buscar_BD_Fecha)
   

    mb1.grid(row=0,column=1)
    
    
    mb1=Menubutton(bottomframe, text="Estadisticas", relief=RAISED )
    mb1.menu =Menu(mb1, tearoff = 0 )
    mb1["menu"]=mb1.menu

    mb1.menu.add_command(label="Temas mas populares",command=fp.popularesBD)
    mb1.menu.add_command(label="Temas mas activos",command=fp.activosBD)
   

    mb1.grid(row=0,column=2)
    
    #DESC
    
    root.mainloop()