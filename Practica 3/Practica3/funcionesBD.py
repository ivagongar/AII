import sqlite3


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
    
def getNumRows():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
       
    cursor=conn.execute("SELECT COUNT(*) FROM FORO")
    
    numRows = str(cursor.fetchone()[0])
    
    conn.close()
    
    return numRows
        
    
def insertRow(titulo,autor, fecha,enlace,respuestas,visitas):
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    conn.execute("""INSERT INTO FORO(TITULO,AUTOR,FECHA,ENLACE,RESPUESTAS,VISITAS) VALUES(?,?,?,?,?,?);""",(titulo,autor,fecha,enlace,respuestas,visitas))
    conn.commit()
    
    conn.close()
    
def selectAll():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor = conn.execute("""SELECT * FROM FORO """)
    
    conn.close()
    
    return cursor
   
def selectPopulares():  
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY VISITAS DESC LIMIT 5""") 
    
    conn.close()
    
    return cursor

def selectActivos():
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("""SELECT * FROM FORO ORDER BY RESPUESTAS DESC LIMIT 10 """)
    
    conn.close()
    
    return cursor

def findTitulo(titulo):
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE TITULO LIKE '%"+titulo+"%'")
    
    conn.close()
    
    return cursor

def findAutor(autor):
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE AUTOR LIKE '%"+autor+"%'") 
    
    conn.close()
    
    return cursor

def findFecha(fecha):
    conn= sqlite3.connect("foro.db")
    conn.text_factory= str
    
    cursor=conn.execute("SELECT * FROM FORO WHERE FECHA LIKE '%"+fecha+"%' ")  
    
    conn.close()
    
    return cursor

    
