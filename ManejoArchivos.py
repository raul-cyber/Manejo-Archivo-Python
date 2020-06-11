import funciones as fun
import logging as log
from tkinter import filedialog
from tkinter import Tk
from tkinter import Button
from tkinter import Entry
from tkinter import StringVar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import INSERT
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import PhotoImage
from tkinter import Label
from tkinter import END


class Aplicacion:

    
    def __init__(self):
        self.template = Tk()
        self.ubicacion = StringVar()
        self.template.title ("Manipulación de archivo")
        self.template.geometry('1100x600')
        self.logo = PhotoImage(file= './img/logo.png')
        Label(self.template, image= self.logo).place(x=0,y=0) 
        self.busqueda = Button(self.template, text="Buscar documento", command=self.CaptarRuta)
        self.busqueda.grid(column = 0, row = 1 , pady = 20)
        self.ruta = Entry(self.template, width = 50 , textvariable = self.ubicacion)
        self.ruta.grid(column = 0 , row = 2 )
        self.ejecutar = Button(self.template, text ="Ejecutar Reparacion y Generacion de Reportes", command = self.iniciar)
        self.ejecutar.grid(column = 0 , row = 3 , padx= 30, pady= 10)
        self.Ejecucion = scrolledtext.ScrolledText(self.template, width = 120, height = 20)
        self.Ejecucion.grid(column = 0, row = 5, padx= 100 , pady = 100)
        self.template.mainloop()
    
    def CaptarRuta(self):
        self.documento = filedialog.askopenfilename()
        self.ubicacion.set(self.documento)

    def ResumenPros(self):

        self.Ejecucion.insert(INSERT,'Documento con Formato Correcto\n')
        log = fun.lectura(str(self.ubicacion.get()))
        self.Ejecucion.insert(INSERT,log)
        
    def iniciar(self):
        self.Ejecucion.delete(1.0, END)
        if(len(self.ubicacion.get()) == 0):
            messagebox.showinfo('Falta Un campo','Es necesario seleccionar un archivo para iniciar el proceso.')
        else:
            self.Ejecucion.insert(INSERT,'************* Iniciando Proceso ************* \n')
            self.Ejecucion.insert(INSERT,'Analizando documento: '+str(self.ubicacion.get())+'\n')
            validacion = fun.ValidarDocumento(str(self.ubicacion.get()))
            if( validacion == 1):
                self.ResumenPros()
            else:
                self.Ejecucion.insert(INSERT,'Documento con Formato Incorrecto\n'+
                'Favor Revisar o Intentar con otro Documento con el formato esperado: \n'+
                'col1;col2;col2;col4........etc')
            
   
        
if __name__ == '__main__':
    Ejecucion = Aplicacion()