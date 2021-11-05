import json
import os
import cv2
from PIL import Image as Img
from PIL import ImageTk
import imutils
import sqlite3

from tkinter import Entry,  StringVar, Label, Button, Tk, messagebox, ttk

class MonitoreaCamara:

    ################ MENÚ USUARIO – MONITOREAR CÁMARA ###############
    def __init__(self, args):

        #Conecta a la BD
        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c = self.db.cursor()
        self.c1 = self.db.cursor()
        self.c2 = self.db.cursor()
        

        #Selecciona el id_camara de la tabla de Usuario
        self.c.execute("SELECT DISTINCT id_camara FROM Usuario")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.result = []
        for row in self.c.fetchall():
            self.result.append(row[0])

        #Selecciona la marca del auto de la tabla de MarcaModelo
        self.c1.execute("SELECT DISTINCT Marca FROM MarcaModelo ORDER BY Marca ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultMarca = []
        for row in self.c1.fetchall():
            self.resultMarca.append(row[0])

        #Lista para guardar los valores de los modelos de autos
        self.listaModelo = []

        #Lista para guardar los valores de los colores
        self.listaColores = ['Amarillo', 'Azul', 'Blanco', 'Cafe', 'Dorado', 'Gris',   
                             'Morado', 'Naranja', 'Negro', 'Rojo', 'Rosa', 'Verde', 'Vino']

        self.windowSubmenuMonitoreaCamara = Tk()
        self.windowSubmenuMonitoreaCamara.geometry("850x500+500+250")
        self.windowSubmenuMonitoreaCamara.title("Menu Usuario/Monitorear Cámara")
        Label(self.windowSubmenuMonitoreaCamara, text = "Monitorear Cámara" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        
        #COLUMNA DE COMBOBOX    
        Label(self.windowSubmenuMonitoreaCamara, text = "Seleccionar Cámara:").place(x=5, y=45)
        self.camara = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values = self.result)
        self.camara.set("Elige una opción")
        self.camara.place(x=120, y=45, width=130, height=25)
        self.btnVisualizar = Button(self.windowSubmenuMonitoreaCamara, text="Visualizar video", command=self.visualizarVideo)
        self.btnVisualizar.place(x=260, y=45, width=100, height=25)

        #COLUMNA DE VALORES
        Label(self.windowSubmenuMonitoreaCamara, text = "Datos de la placa detectada" ).place(x=5, y=95)

        Label(self.windowSubmenuMonitoreaCamara, text = "Placa" ).place(x=5, y=130)
        self.entryPlaca_var = StringVar()
        self.entryPlaca = Entry(self.windowSubmenuMonitoreaCamara, textvariable = self.entryPlaca_var)
        self.entryPlaca.place(x=5, y=150, width=160, height=25)

        Label(self.windowSubmenuMonitoreaCamara, text = "Marca" ).place(x=5, y=180)
        self.comboMarca = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=5, y=200, width=160, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuMonitoreaCamara, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=10, y=230, width=160, height=30)

        Label(self.windowSubmenuMonitoreaCamara, text = "Modelo" ).place(x=5, y=270)
        self.comboModelo = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=5, y=290, width=160, height=25)

        Label(self.windowSubmenuMonitoreaCamara, text = "Color" ).place(x=5, y=320)
        self.comboColor = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=5, y=340, width=160, height=25)

        self.lblVideo = Label(self.windowSubmenuMonitoreaCamara, text = "" )
        self.lblVideo.place(x=185, y=105)

        #COLUMNA DE BOTONES
        self.buttonGenerar = Button(self.windowSubmenuMonitoreaCamara, text = "Generar Reporte de Alerta", command = self.generarReporteAlerta)
        self.buttonGenerar.place(x=10, y=380, width=160, height=30 )
        #self.buttonVisualizar = Button(self.windowSubmenuMonitoreaCamara, text = "Visualizar Alerta", command = lambda : VisualizarReporteAlerta.visualizarAlerta(self, self.windowSubmenuMonitoreaCamara.withdraw()))
        #self.buttonVisualizar.place(x=10, y=260, width=120, height=30)
        #self.buttonRegresar = Button(self.windowSubmenuMonitoreaCamara, text = "Regresar", command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        #self.buttonRegresar.place(x=10, y=420, width=160, height=30)
        
        self.windowSubmenuMonitoreaCamara.mainloop()

    def monitorearCamara(self):
        pass

    def generarReporteAlerta(self):

        if self.entryPlaca.get() == "" or len(self.entryPlaca.get()) > 9 or len(self.entryPlaca.get()) < 7:
            if self.entryPlaca.get() == "":
                return messagebox.showwarning("Genear Reporte","Error, campo Placa no puede ir vacio")
            elif len(self.entryPlaca.get()) > 9:
                return messagebox.showwarning("Genear Reporte","Error, campo Placa excede caracteres permitidos")
            else:
                return messagebox.showwarning("Genear Reporte","Error, campo Placa debe tener al menos 7 caracteres")
        elif self.comboMarca.get() == "Marca":
            return messagebox.showwarning("Genear Reporte","Error, selecciona una marca")
        elif self.comboModelo.get() == "Modelo":
            return messagebox.showwarning("Genear Reporte","Error, selecciona un modelo")
        elif self.comboColor.get() == "Color":
            return messagebox.showwarning("Genear Reporte","Error, selecciona un color")

        data_dict =  {
            "Placa"  : f"{self.entryPlaca.get().upper()}",
            "Marca"  : f"{self.comboMarca.get()}",
            "Modelo" : f"{self.comboModelo.get()}",
            "Color"  : f"{self.comboColor.get()}"
            }

        fname = "ReporteAlerta.json"
        if os.path.isfile(fname):
            # File exists
            with open(fname, 'a+') as outfile:
                outfile.seek(0, os.SEEK_END)
                outfile.seek(outfile.tell()  - 1, os.SEEK_SET)
                outfile.truncate()
                outfile.write(',')
                json.dump(data_dict, outfile)
                outfile.write('\n]')
        else: 
            # Create file
            with open(fname, 'w') as outfile:
                array = []
                array.append(data_dict)
                json.dump(array, outfile)

        self.entryPlaca.delete(0, 'end')
        self.comboMarca.set("Marca")
        self.comboModelo.set("Modelo")
        self.comboColor.set("Color")

        messagebox.showinfo("Genear Reporte","Reporte de alerta generado con éxito")

    def obtenerModelo(self): 
        if self.comboMarca.get() == "Marca":
            return messagebox.showwarning("Genear Reporte","Error, selecciona una marca")

        self.valor = self.comboMarca.get()
        
        self.c2.execute("SELECT Modelo FROM MarcaModelo WHERE Marca = ? ORDER BY Modelo ASC", (self.valor,))
        
        if self.listaModelo == []:
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])
        else:
            del self.listaModelo [:]
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])

        #print ("dentro self.listaModelo - obtenerModelo:", self.listaModelo)
        self.db.commit
        self.comboModelo ["values"] = self.listaModelo
        self.comboModelo.set("Modelo")

    def visualizarVideo(self):
        self.cap = None

        if self.cap is not None:
            self.lblVideo.image = ""
            self.cap.release()
            self.cap = None

        self.video_path = ''
        if  self.camara.get() == "1":
            self.video_path = "autos1.mp4"
            self.cap = cv2.VideoCapture(self.video_path)
            self.visualizar()
        elif self.camara.get() == "2":
            self.video_path = "autos2.mp4"
            self.cap = cv2.VideoCapture(self.video_path)
            self.visualizar()
        else:
            messagebox.showwarning("Visualizar video","No se seleccionó cámara")

    def visualizar(self):
        if self.cap is not None:
            self.ret, self.frame = self.cap.read()
            if self.ret == True:
                self.frame = imutils.resize(self.frame, width=640)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                self.im = Img.fromarray(self.frame)
                self.img = ImageTk.PhotoImage(image=self.im)

                self.lblVideo.configure(image=self.img)
                self.lblVideo.image = self.img
                self.lblVideo.after(10, self.visualizar)
            else:
                print("No se selecciono nada")
                self.lblVideo.image = ""
                self.cap.release()
        

args = ""
MonitoreaCamara(args)
