import sqlite3
from tkinter import Text, messagebox, Label, Button, Tk, ttk
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
            

        self.windowSubmenuRPObtenerReporteAlerta = Tk()
        self.windowSubmenuRPObtenerReporteAlerta.geometry("350x300+500+250")
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
        self.textReporteGenerado.place(x=5, y=140,  width=330, height=100)

        #COLUMNA DE BOTONES
        self.buttonGuardar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Guardar", command = self.obtieneReporteAlerta)
        self.buttonGuardar.place(x=50, y=250, width=100, height=30) #AQUI PORNER UN MENSAJE DE SE GUARDO CORRECTAMENTE,
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar")#, command = lambda : ReportePlacas(self.windowSubmenuRPObtenerReporteAlerta.withdraw())
        self.buttonRegresar.place(x=200, y=250, width=100, height=30)

        self.windowSubmenuRPObtenerReporteAlerta.mainloop()


    def buscaReporteAlerta(self):
        self.textReporteGenerado.delete('1.0', tk.END)
        
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")
        #else:
        #    print(self.comboPlaca.get())

        self.db = sqlite3.connect('proyecto_placas_pruebas.db')
        self.c1 = self.db.cursor()       

        #Selecciona valores de la tabla de Camara 
        self.c1.execute("SELECT idCamara, calle, colonia, delegacion FROM Camara WHERE idCamara = ?", (config.camara)) 
        
        self.result = []
        for row in self.c1.fetchall():
            self.result.append(row) 
        print(self.result)
        
        
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file)
            
            for profile in profiles:
                if profile["Placa"] == self.comboPlaca.get():
                    profile1 = json.dumps(profile, indent=4, sort_keys=False)#Imprime bonito el JSON
                    #profile1.truncate()
                    #profile1.write(self.result)
                    #json.dump(profile1, self.result)
                    self.textReporteGenerado.insert('1.0', profile1)#inserta valor en el widget text
        
        idCamara = self.result[0][0]

        idCamara_var = "Id Camara: ", idCamara
        calle_var = f"Calle:{self.result[0][1]}\n"
        colonia_var = f"Colonia:{self.result[0][2]}\n"
        delegacion_var = f"Alcaldia:{self.result[0][3]}\n"

        datosCamara = idCamara, calle_var, colonia_var, delegacion_var
        self.textReporteGenerado.insert('1.0', datosCamara)#inserta valor en el widget text

            
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")
        #self.comboPlaca.set("Placa")

    def obtieneReporteAlerta(self):
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        file = open(f"./ObtenerReporteVisualizacion_Guardados/{self.comboPlaca.get()}.txt", "w")
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


