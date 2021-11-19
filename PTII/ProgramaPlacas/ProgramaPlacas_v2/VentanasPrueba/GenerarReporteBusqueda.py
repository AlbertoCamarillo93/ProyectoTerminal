import sqlite3
from tkinter import *
from tkinter import ttk, Tk
import tkinter
import os
import json
from tkinter import messagebox

class GenerarReporteBusqueda:

    def __init__(self, args):
        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c1 = self.db.cursor()
        self.c2 = self.db.cursor()

        #Selecciona la marca del auto de la tabla de MarcaModelo
        self.c1.execute("SELECT DISTINCT Marca FROM MarcaModelo ORDER BY Marca ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultMarca = []
        for row in self.c1.fetchall():
            self.resultMarca.append(row[0])

        #Lista para guardar los valores de los modelos de autos
        self.listaModelo = []

        #Lista con los valores de los colores
        self.listaColores = ['Amarillo', 'Azul', 'Blanco', 'Cafe', 'Dorado', 'Gris',   
                             'Morado', 'Naranja', 'Negro', 'Rojo', 'Rosa', 'Verde', 'Vino']
        self.listaAbecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', 'Ñ','O',
                                'P','Q','R','S','T','U','V','W','X','Y','Z',
                                'a','b','c','d','e','f','g','h','i','j','k','l','m','n', 'ñ','o',
                                'p','q','r','s','t','u','v','w','x','y','z']
        self.listaNumeros = ['0','1','2','3','4','5','6','7','8','9']

        self.windowSubmenuRPGenerarReporte = Tk()
        self.windowSubmenuRPGenerarReporte.geometry("350x300+500+250")
        self.windowSubmenuRPGenerarReporte.title("Reporte de Placas/Generar Reporte")
        Label(self.windowSubmenuRPGenerarReporte, text = "Generar Reporte" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)


        ####CAMBIO --> radiobutton
        #RADIOBUTTON
        self.opcion = IntVar()
        self.buttonCDMX = Radiobutton(self.windowSubmenuRPGenerarReporte, text="Ciudad de México", variable= self.opcion, value=1, command= self.selectRadioButton)
        self.buttonCDMX.place(x=20, y=45)
        self.buttonEdoMex = Radiobutton(self.windowSubmenuRPGenerarReporte, text="Estado de México", variable= self.opcion, value=2, command= self.selectRadioButton)
        self.buttonEdoMex.place(x=160, y=45)
        ####CAMBIO

        #COLUMNA DE LABES, BOXES
        Label(self.windowSubmenuRPGenerarReporte, text = "Placa:" ).place(x=5, y=70)
        self.boxPlate_var = StringVar()
        self.boxPlate = Entry(self.windowSubmenuRPGenerarReporte, textvariable = self.boxPlate_var)
        self.boxPlate.place(x=105, y=70, width=180, height=25)

        Label(self.windowSubmenuRPGenerarReporte, text = "Marca:" ).place(x=5, y=105)
        self.comboMarca = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=105, y=105, width=180, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuRPGenerarReporte, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=120, y=140, width=140, height=30)

        Label(self.windowSubmenuRPGenerarReporte, text = "Modelo:" ).place(x=5, y=180)
        self.comboModelo = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=105, y=180, width=180, height=25)

        Label(self.windowSubmenuRPGenerarReporte, text = "Color:" ).place(x=5, y=215)
        self.comboColor = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=105, y=215, width=180, height=25)

        #COLUMNA DE BOTONES
        self.buttonAceptar = Button(self.windowSubmenuRPGenerarReporte, text = "Aceptar", command = self.generarReporteBusqueda)
        self.buttonAceptar.place(x=105, y=250,  width=80, height=30)
        self.buttonRegresar = Button(self.windowSubmenuRPGenerarReporte, text = "Regresar")#, command = lambda : ReportePlacas(self.windowSubmenuRPGenerarReporte.withdraw()))
        self.buttonRegresar.place(x=200, y=250, width=80, height=30)

        self.windowSubmenuRPGenerarReporte.mainloop()

    def generarReporteBusqueda(self):

        #if self.boxPlate.get() == "" or len(self.boxPlate.get()) > 9 or len(self.boxPlate.get()) < 7:
        ####CAMBIO --> Reorganización
        if self.boxPlate.get() == "":
            return messagebox.showerror("Genear Reporte","Error, campo Placa no puede ir vacio")
        elif len(self.boxPlate.get()) > 9:
            return messagebox.showerror("Genear Reporte","Error, campo Placa excede caracteres permitidos")
        elif len(self.boxPlate.get()) < 7:
            return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener al menos 7 caracteres")
        
        #Placa CDMX
        if self.opcion.get() == 1:
            len(self.boxPlate.get()) == 7
            for indice in range(len(self.boxPlate.get())):
                caracter = '-'
                if self.boxPlate.get()[0] not in self.listaNumeros and self.boxPlate.get()[0] not in self.listaAbecedario:
                     return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener letra o número en la posición 1")
                elif self.boxPlate.get()[1] not in self.listaNumeros or self.boxPlate.get()[2] not in self.listaNumeros:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener número en la posición 2 y 3")
                elif caracter != self.boxPlate.get()[3]:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener \"-\" en la tercer posición")
                elif self.boxPlate.get()[4] not in self.listaAbecedario or self.boxPlate.get()[5] not in self.listaAbecedario or self.boxPlate.get()[6] not in self.listaAbecedario:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener letra en los últimos tres caractéres")
                    
        
        #Placa EdoMex
        if self.opcion.get() == 2:
            len(self.boxPlate.get()) == 9
            for indice in range(len(self.boxPlate.get())):
                caracter = '-'
                if caracter != self.boxPlate.get()[3] or caracter != self.boxPlate.get()[6]:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener \"-\" en la cuarta y séptima posición")
                elif self.boxPlate.get()[0] not in self.listaAbecedario or self.boxPlate.get()[1] not in self.listaAbecedario or self.boxPlate.get()[2] not in self.listaAbecedario:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener letra en los primeros tres caracteres")
                elif self.boxPlate.get()[4] not in self.listaNumeros or self.boxPlate.get()[5] not in self.listaNumeros or self.boxPlate.get()[7] not in self.listaNumeros or self.boxPlate.get()[8] not in self.listaNumeros:
                    return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener número en la posición 5,6,8,9")
        ####CAMBIO

        if self.comboMarca.get() == "Marca": ####CAMBIO elif --> if
            return messagebox.showerror("Genear Reporte","Error, selecciona una marca")
        elif self.comboModelo.get() == "Modelo":
            return messagebox.showerror("Genear Reporte","Error, selecciona un modelo")
        elif self.comboColor.get() == "Color":
            return messagebox.showerror("Genear Reporte","Error, selecciona un color")

        data_dict =  {
            "Placa"  : f"{self.boxPlate.get().upper()}",
            "Marca"  : f"{self.comboMarca.get()}",
            "Modelo" : f"{self.comboModelo.get()}",
            "Color"  : f"{self.comboColor.get()}"
            }

        fname = "PlacasReporteBusqueda.json"
        if os.path.isfile(fname):
            # File exists
            with open(fname, 'a+') as outfile:
                outfile.seek(0, os.SEEK_END)
                outfile.seek(outfile.tell()  - 5, os.SEEK_SET)
                outfile.truncate()
                outfile.write(',')
                json.dump(data_dict, outfile)
                outfile.write('\n]')
                outfile.write('\n}')
        else: 
            # Create file
            with open(fname, 'w') as outfile:
                array = []
                array.append(data_dict)
                json.dump(array, outfile)

        self.boxPlate.delete(0, 'end')
        self.comboMarca.set("Marca")
        self.comboModelo.set("Modelo")
        self.comboColor.set("Color")

        messagebox.showinfo("Genear Reporte","Reporte generado con éxito")

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
        self.comboModelo ["values"]= self.listaModelo
        self.comboModelo.set("Modelo")

    ####CAMBIO --> funcion nueva
    def selectRadioButton(self):
        if self.opcion.get() == 1:
            print("CDMX")
            self.boxPlate_var.set("A00-AAA / 000-AAA")
        else:
            print("EDOMEX")
            self.boxPlate_var.set("AAA-00-00")     
    ####CAMBIO

args = ""
GenerarReporteBusqueda(args)