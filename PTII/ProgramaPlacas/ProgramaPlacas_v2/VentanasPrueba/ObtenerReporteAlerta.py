import sqlite3
from tkinter import Text, Toplevel, messagebox, Label, Button, Tk, ttk
import json
import tkinter as tk
import config
import os

class ObtenerReporteAlerta:
    
    ################ ADMINISTRADOR – REPORTE DE PLACAS – OBTENER REPORTE ###############
    def __init__(self, args):
        self.listaPlacas = []
        with open('ReporteAlerta.json', 'r') as file:
            placasJson = json.load(file)
            for self.placaJson in placasJson:
                self.listaPlacas.append(self.placaJson["Placa"])
            self.listaPlacas.sort()
            

        self.windowSubmenuRPObtenerReporteAlerta = Toplevel()

        ancho_ventana = 350
        alto_ventana = 400
        x_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.windowSubmenuRPObtenerReporteAlerta.geometry(posicion)

        self.windowSubmenuRPObtenerReporteAlerta.title("Reporte de Placas/Obtener Reporte")
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Obtener Reporte Alerta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE LABES, BOXES
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Ingresa la placa para obtener el reporte:" ).place(x=5, y=45)
       
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Placa:" ).place(x=5, y=75)
        self.comboPlaca = ttk.Combobox(self.windowSubmenuRPObtenerReporteAlerta,  state = "readonly")
        self.comboPlaca ["values"] = self.listaPlacas
        self.comboPlaca.set("Placa")
        self.comboPlaca.place(x=50, y=75, width=130, height=30)

        self.buttonAceptar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Aceptar", command = self.buscaReporteAlerta)
        self.buttonAceptar.place(x=200, y=75, width=80, height=30)

        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "El reporte generado es:" ).place(x=5, y=110)
        self.textReporteGenerado = Text(self.windowSubmenuRPObtenerReporteAlerta, state = "normal")
        self.textReporteGenerado.place(x=5, y=140,  width=330, height=180)

        #COLUMNA DE BOTONES
        self.buttonGuardar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Guardar", command = self.obtieneReporteAlerta)
        self.buttonGuardar.place(x=50, y=340, width=100, height=30) #AQUI PORNER UN MENSAJE DE SE GUARDO CORRECTAMENTE,
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar")#, command = lambda : ReportePlacas(self.windowSubmenuRPObtenerReporteAlerta.withdraw())
        self.buttonRegresar.place(x=200, y=340, width=100, height=30)

        self.windowSubmenuRPObtenerReporteAlerta.mainloop()


    def buscaReporteAlerta(self):
        self.textReporteGenerado.delete('1.0', tk.END)
        
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")
        #else:
        #    print(self.comboPlaca.get())

        self.db = sqlite3.connect('proyecto_placas_pruebas.db')
        self.c1 = self.db.cursor()       
       
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file)
       
            for profile in profiles:
                if profile["Placa"] == self.comboPlaca.get():
                    self.camaraSalvar = profile['Camara']
                    print('camaraSalvar:', profile['Camara'])
                    profile1 = json.dumps(profile, indent=4, sort_keys=False)#Imprime bonito el JSON
                    self.textReporteGenerado.insert('1.0', profile1)#inserta valor en el widget text
            
            for client in profiles:
                if client['Placa'] == self.comboPlaca.get():
                    self.placaSalvar = client['Placa']
                    print('PlacaSalvar:', client['Placa'])

            #Selecciona valores de la tabla de Camara 
            self.c1.execute("SELECT idCamara, calle, colonia, delegacion FROM Camara WHERE idCamara = ?", (self.camaraSalvar)) 
            
            self.result = []
            for row in self.c1.fetchall():
                self.result.append(row) 
            print(self.result)

        idCamara = self.result[0][0]
        calle = self.result[0][1]
        colonia = self.result[0][2]
        alcaldia = self.result[0][3]

        self.textReporteGenerado.insert('1.0', f"idCamara: {idCamara}\nCalle: {calle}\nColonia: {colonia}\nAlcaldia: {alcaldia}\n")#inserta valor en el widget text

            
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")
        #self.comboPlaca.get()

    def obtieneReporteAlerta(self):
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        file = open(f"./ObtenerReporteVisualizacion_Guardados/{self.placaSalvar}.txt", "w")
        file.write(f"{self.datosGuardarTxt}")
        #file.close()
        self.textReporteGenerado.delete('1.0', tk.END)

        self.comboPlaca ["values"]= self.listaPlacas
        self.comboPlaca.set("Placa")

        return messagebox.showinfo("Guardar Reporte","Registro guardado con éxito")

            

args = ""   
ObtenerReporteAlerta(args)


config.apellido = ObtenerReporteAlerta.obtieneVariablesGlobales(args)
config.camara = ObtenerReporteAlerta.obtieneVariablesGlobales(args)
config.contacto_usuario = ObtenerReporteAlerta.obtieneVariablesGlobales(args)
config.id_usuario = ObtenerReporteAlerta.obtieneVariablesGlobales(args)
config.nombre = ObtenerReporteAlerta.obtieneVariablesGlobales(args)


