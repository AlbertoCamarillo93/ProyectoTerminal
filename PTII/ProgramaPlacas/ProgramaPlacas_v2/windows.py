import json
import os
import cv2
from PIL import Image as Img
from PIL import ImageTk
import imutils
import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox


class Login:

    #EL MÉTODO __init__ ES UN CONSTRUCTOR, Y SIEMPRE LLEVA AL MENOS UN ARGUMENTO (self).
    #ESTE MÉTDOO, TIENE TAMBIÉN COMO FUNCIÓN DECLARAR LOS VALORES DE INICIO DE LAS VARIABLES DE CLASE, ES DECIR, INICIALIZAR LAS VARIABLES, PARA LOGRAR ESTO,
    #SE DECLARAN LOS ARGUMENTOS QUE SEAN NECESARIOS.
    #CUANDO SE INVOCA ESTE MÉTODO, SE CUENTAN TODOS LOS PARAMENTROS QUE TENGA, MENOS SELF
    def __init__(self, args):
        #BLOQUE INTERFAZ
        self.windowLogin = Tk() #Crea una instancia de tkinter
        self.windowLogin.title ("Iniciar Sesión")
        self.windowLogin.geometry ("350x150+500+250")

        #CORREO
        Label(self.windowLogin, text = "Correo:").pack()
        self.boxEmail = Entry(self.windowLogin)
        self.boxEmail.pack()

        #PASSWORD
        Label(self.windowLogin, text = "Contraseña:").pack()
        self.boxPassword = Entry(self.windowLogin, show = "*")
        self.boxPassword.pack()

        self.buttonLogin = Button (self.windowLogin, text = "Login", command = self.login).pack()
        self.buttonExit = Button (self.windowLogin, text = "Salir", command = self.exit).pack()

        self.windowLogin.mainloop() #EJECUTA LA VENTANA PRINCIPAL


    #FUNCIÓN BOTÓN DE LOGEO
    def login(self):
        # Connect to database
        self.db = sqlite3.connect('proyecto_placas.db')
        self.c = self.db.cursor()
        
        self.c.execute("SELECT * FROM Usuario WHERE correo=? AND password=?", (self.boxEmail.get(), self.boxPassword.get()))
        
        row = self.c.fetchall() 
        if row:
            if row[0][6] == 'Administrador':
                Administrador(self)
                self.windowLogin.withdraw() 
            elif row[0][6] == 'Usuario':
                User(self)
                self.windowLogin.withdraw()
        else:
            tkinter.messagebox.showerror(title = "Login incorrecto", message = "Usuario o contraseña incorrecta")
    
        self.c.close()
        #print(row)

    def prueba(self):
        self.boxEmail.get()
    def exit(self):
        self.windowLogin.destroy()


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class Administrador():

    def __init__(self, args):
        self.windowMenuAdmin = Tk()
        self.windowMenuAdmin.geometry("350x200+500+250")
        self.windowMenuAdmin.title("Menu Administrador")
        Label(self.windowMenuAdmin, text = "Menu Administrador" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        
        #COLUMNA DE ETIQUETAS
        Label(self.windowMenuAdmin, text = "ID_Usuario" ).place(x=5, y=45)
        Label(self.windowMenuAdmin, text = "Nombre" ).place(x=5, y=75)
        Label(self.windowMenuAdmin, text = "Datos Contacto" ).place(x=5, y=105)


        #COLUMNA DE BOTONES
        self.buttonGestionarUsuario = Button(self.windowMenuAdmin, text = "Gestión de usuarios", command = lambda : GestionarUsuario(self.windowMenuAdmin.withdraw()))
        self.buttonGestionarUsuario.place(x=200, y=45, width=120, height=30)

        self.buttonReportePlacas = Button(self.windowMenuAdmin, text = "Reporte de placas", command = lambda : ReportePlacas(self.windowMenuAdmin.withdraw()))
        self.buttonReportePlacas.place(x=200, y=90, width=120, height=30) 

        self.buttonCerrarSesion = Button(self.windowMenuAdmin, text = "Cerrar Sesión", command = lambda : Login(self.windowMenuAdmin.withdraw()))
        self.buttonCerrarSesion.place(x=240, y=160, width=100, height=30)
        

    def menuAdmin(self):
        pass       


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class User():
    
    def __init__(self, args):   
        #Login.prueba(self)
        self.windowMenuUser = Tk()
        self.windowMenuUser.geometry("400x300+500+250")
        self.windowMenuUser.title("Menu Usuario")
        Label(self.windowMenuUser, text = "Menu Usuario" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    
        #COLUMNA DE ETIQUETAS
        Label(self.windowMenuUser, text = "ID_Usuario" ).place(x=5, y=45)
        Label(self.windowMenuUser, text = "Nombre" ).place(x=5, y=75)
        Label(self.windowMenuUser, text = "Cámara" ).place(x=5, y=105)
        Label(self.windowMenuUser, text = "Datos Contacto" ).place(x=5, y=135)

        #COLUMNA DE BOTONES
        #CREAR CONDICION EN OBTENER REPORTE PARA QUE CUANDO VENGA DESDE EL MENU DE USUARIO NO ME MEZCLE CON EL MENU DE ADMINISTRADOR
        #LLAMA CLASE ObtenerReporteAlerta, pero esta también es llamada por el Admin, realizar lógica para que tanto admin como user 
        #puedan entrar y no haya conflicto de ventanas
        self.buttonReporteAlerta = Button(self.windowMenuUser, text = "Obtener Reporte de Alertas", command = lambda : ObtenerReporteAlertaUsuario(self.windowMenuUser.withdraw()))  #, command = obtenerReporte
        self.buttonReporteAlerta.place(x=200, y=45, width=180, height=30) 

        self.buttonMonitorearCamara = Button(self.windowMenuUser, text = "Monitorear Cámara", command = lambda : MonitoreaCamara(self.windowMenuUser.withdraw()))
        self.buttonMonitorearCamara.place(x=200, y=90, width=180, height=30)

        self.buttonCerrarSesion = Button(self.windowMenuUser, text = "Cerrar Sesión", command = lambda : Login(self.windowMenuUser.withdraw()))
        self.buttonCerrarSesion.place(x=270, y=260, width=100, height=30)


    def  menuUser(self, args):
        pass

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class GestionarUsuario():
    
    def __init__(self, args):
        self.windowSubmenuGestionUsuarios = Tk()
        self.windowSubmenuGestionUsuarios.geometry("350x200+500+250")
        self.windowSubmenuGestionUsuarios.title("Gestión Usuarios")

        Label( self.windowSubmenuGestionUsuarios, text = "Gestión Usuarios" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE BOTONES
        self.buttonCrear = Button( self.windowSubmenuGestionUsuarios, text = "Crear Cuenta", command = lambda : GestionarUsuarioCrear(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonCrear.pack(padx= 5, pady = 5, ipadx = 15, ipady = 5)

        self.buttonModificar = Button( self.windowSubmenuGestionUsuarios, text = "Modificar Cuenta", command = lambda : GestionarUsuarioModificar(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonModificar.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5) 

        self.buttonEliminar = Button( self.windowSubmenuGestionUsuarios, text = "Eliminar Cuenta",  command =  lambda : GestionarUsuarioElimina(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonEliminar.pack(padx= 5, pady = 5, ipadx = 10, ipady = 5)

        self.buttonregresar = Button( self.windowSubmenuGestionUsuarios, text = "Regresar", command = lambda : Administrador(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonregresar.place(x=260, y=160, width=80, height=30) 


    ################ ADMINISTRADOR – GESTIÓN DE USUARIOS ###############
    def gestionUsuarios(self):
        pass

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class GestionarUsuarioElimina():

    def __init__(self, args):

        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c = self.db.cursor()
        self.c.execute("SELECT correo FROM Usuario ORDER BY correo ASC ")   

        self.result = []

        for row in self.c.fetchall():
            self.result.append(row[0])

        self.windowSubmenuGUEliminarCuenta = Tk()
        self.windowSubmenuGUEliminarCuenta.geometry("350x300+500+250")
        self.windowSubmenuGUEliminarCuenta.title("Gestión Usuarios/Eliminar Cuenta")
        Label(self.windowSubmenuGUEliminarCuenta, text = "Eliminar Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE COMBOBOX
        Label( self.windowSubmenuGUEliminarCuenta, text = "Eliminar Cuenta:").place(x=5, y=45) 
        self.comboEliminar = ttk.Combobox( self.windowSubmenuGUEliminarCuenta, state = "readonly", values = self.result) 
        self.comboEliminar.set("Elige una opción")
        self.comboEliminar.place(x=105, y=45, width=130, height=30)        
        
        #COLUMNA DE BOTONES
        self.buttonConfirmar = Button( self.windowSubmenuGUEliminarCuenta, text = "Confirmar", command = self.eliminarCuenta)
        self.buttonConfirmar.place(x=70, y=95, width=80, height=30)
        
        self.buttonRegresar = Button(self.windowSubmenuGUEliminarCuenta, text = "Regresar", command = lambda : GestionarUsuario(self.windowSubmenuGUEliminarCuenta.withdraw()))
        self.buttonRegresar.place(x=190, y=95, width=80, height=30)

    def eliminarCuenta(self):
        if self.comboEliminar.get() == "Elige una opción":
                return messagebox.showwarning("Eliminar Usuario","Error, selecciona un usuario")

        self.c1 = self.db.cursor()
        self.valor = self.comboEliminar.get()
        self.c1.execute("DELETE FROM Usuario WHERE correo = ?", (self.valor,))                 
        self.db.commit()

        self.comboEliminar.set("Elige una opción")
        
        messagebox.showinfo("Eliminar Usuario","Registro borrado con éxito") 
        


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class GestionarUsuarioCrear:
    
    ################ ADMINISTRADOR - GESTIÓN DE USUARIOS – CREAR CUENTA ###############
    def __init__(self, args):
        #Conexión bd
        self.db = sqlite3.connect('proyecto_placas.db')
        self.c1 = self.db.cursor()
        self.c2 = self.db.cursor()     

        #Selecciona el id_camara de la tabla de Usuario para llamarlo en self.comboAsignarCamara
        self.c1.execute("SELECT DISTINCT id_camara FROM Usuario ORDER BY id_camara ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultCamara = []
        for row in self.c1.fetchall():
            self.resultCamara.append(row[0])

        #Selecciona el tipo de usuario a crear para llamarlo en self.comboTipoUsuario
        self.c2.execute("SELECT DISTINCT tipoUsuario FROM Usuario ORDER BY tipoUsuario ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultTipoUser = []
        for row in self.c2.fetchall():
            self.resultTipoUser.append(row[0])

        self.windowSubmenuGUCrearCuenta = Tk()
        self.windowSubmenuGUCrearCuenta.geometry("350x300+500+250")
        self.windowSubmenuGUCrearCuenta.title("Gestión Usuarios/Crear Cuenta")
        Label(self.windowSubmenuGUCrearCuenta, text = "Crear Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE LABES Y BOXES
        Label(self.windowSubmenuGUCrearCuenta, text = "Nombre:" ).place(x=5, y=45)
        self.boxName = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxName.place(x=105, y=45, width=180, height=25)

        Label(self.windowSubmenuGUCrearCuenta, text = "Apellido Paterno:" ).place(x=5, y=75)
        self.boxLastname = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxLastname.place(x=105, y=75,  width=180, height=25)

        Label(self.windowSubmenuGUCrearCuenta, text = "Contraseña" ).place(x=5, y=105)
        self.boxPassword = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxPassword.place(x=105, y=105,  width=180, height=25)
        
        Label(self.windowSubmenuGUCrearCuenta, text = "Correo:").place(x=5, y=135)
        self.boxEmail = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxEmail.place(x=105, y=135, width=180, height=25)

        #COLUMNA DE COMBOBOX
        Label(self.windowSubmenuGUCrearCuenta, text = "Tipo Usuario:").place(x=5, y=195)
        self.comboTipoUsuario = ttk.Combobox(self.windowSubmenuGUCrearCuenta, state = "readonly", values = self.resultTipoUser)
        self.comboTipoUsuario.set("Elige una opción")
        self.comboTipoUsuario.place(x=105, y=195, width=180, height=25)

        Label(self.windowSubmenuGUCrearCuenta, text = "Asignar Cámara:").place(x=5, y=165)
        self.comboAsignarCamara = ttk.Combobox(self.windowSubmenuGUCrearCuenta,  state = "readonly", values = self.resultCamara)
        self.comboAsignarCamara.set("Elige una opción")
        self.comboAsignarCamara.place(x=105, y=165, width=180, height=25)
        
        #COLUMNA DE BOTONES
        self.buttonCrear = Button(self.windowSubmenuGUCrearCuenta, text = "Crear", command = self.crearUsuario)
        self.buttonCrear.place(x=110, y=240, width=80, height=30)
        
        self.buttonRegresar = Button(self.windowSubmenuGUCrearCuenta, text = "Regresar", command = lambda : GestionarUsuario(self.windowSubmenuGUCrearCuenta.withdraw()))
        self.buttonRegresar.place(x=200, y=240, width=80, height=30)
               
    #CREAR MENSAJES DE ERROR Y EXITO SEGUN SEA EL CASO
    def crearUsuario(self):
        
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboAsignarCamara.get() == "Elige una opción":
            return messagebox.showwarning("Crear Usuario","Error, ningun campo puede quedar vacio")

        self.c = self.db.cursor()

        self.datos = self.comboAsignarCamara.get(), self.boxName.get(),self.boxLastname.get(),self.boxPassword.get(),self.boxEmail.get(),self.comboTipoUsuario.get()
        self.c.execute("INSERT INTO Usuario VALUES(NULL,?,?,?,?,?,?)", (self.datos))  
            
        self.db.commit()

        self.boxName.delete(0, 'end')
        self.boxLastname.delete(0, 'end')
        self.boxPassword.delete(0, 'end')
        self.boxEmail.delete(0, 'end')
        self.comboTipoUsuario.set("Elige una opción")
        self.comboAsignarCamara.set("Elige una opción")

        messagebox.showinfo("Crear Usuario","Registro insertado con éxito")


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class GestionarUsuarioModificar:  
    ################ ADMINISTRADOR – GESTIÓN DE USUARIO – MODIFICAR CUENTA ###############
    def __init__(self, args):

        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c = self.db.cursor()
        self.c1 = self.db.cursor()
        self.c2 = self.db.cursor() 

        #Selecciona el correo de la tabla de Usuario para llamarlo en self.comboUser
        self.c.execute("SELECT correo FROM Usuario ORDER BY correo ASC ")   

        self.result = []
        for row in self.c.fetchall():
            self.result.append(row[0])            

        #Selecciona el id_camara de la tabla de Usuario para llamarlo en self.comboAsignarCamara
        self.c1.execute("SELECT DISTINCT id_camara FROM Usuario ORDER BY id_camara ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultCamara = []
        for row in self.c1.fetchall():
            self.resultCamara.append(row[0])

        #Selecciona el tipo de usuario a crear para llamarlo en self.comboTipoUsuario
        self.c2.execute("SELECT DISTINCT tipoUsuario FROM Usuario ORDER BY tipoUsuario ASC")   

        #Lista para guardar los valores recorridos en el ciclo for
        self.resultTipoUser = []
        for row in self.c2.fetchall():
            self.resultTipoUser.append(row[0])

        self.windowSubmenuGUModificarCuenta = Toplevel()
        self.windowSubmenuGUModificarCuenta.geometry("350x350+500+250")
        self.windowSubmenuGUModificarCuenta.title("Gestión Usuarios/Modificar Cuenta")
        Label(self.windowSubmenuGUModificarCuenta, text = "Modificar Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE LABES, COMBOBOXES Y BOXES
        Label(self.windowSubmenuGUModificarCuenta, text = "Seleccionar Usuario:").place(x=5, y=45)
        self.comboUser = ttk.Combobox(self.windowSubmenuGUModificarCuenta, state = "readonly", values = self.result)
        self.comboUser.set("Elige una opción")
        self.comboUser.place(x=120, y=45, width=110, height=25)

        self.buttonBuscar = Button(self.windowSubmenuGUModificarCuenta, text = "Buscar", command = self.buscar)
        self.buttonBuscar.place(x=240, y=45, width=80, height=25)


        Label(self.windowSubmenuGUModificarCuenta, text = "Nombre:" ).place(x=5, y=75)
        self.boxName_var = StringVar()
        self.boxName = Entry(self.windowSubmenuGUModificarCuenta, textvariable = self.boxName_var)
        self.boxName.place(x=120, y=75, width=180, height=25)

        Label(self.windowSubmenuGUModificarCuenta, text = "Apellido Paterno:" ).place(x=5, y=105)
        self.boxLastname_var = StringVar()
        self.boxLastname = Entry(self.windowSubmenuGUModificarCuenta, textvariable = self.boxLastname_var)
        self.boxLastname.place(x=120, y=105,  width=180, height=25)

        Label(self.windowSubmenuGUModificarCuenta, text = "Contraseña" ).place(x=5, y=135)
        self.boxPassword_var = StringVar()
        self.boxPassword = Entry(self.windowSubmenuGUModificarCuenta, textvariable = self.boxPassword_var)
        self.boxPassword.place(x=120, y=135,  width=180, height=25)
        
        Label(self.windowSubmenuGUModificarCuenta, text = "Correo:").place(x=5, y=165)
        self.boxEmail_var = StringVar()
        self.boxEmail = Entry(self.windowSubmenuGUModificarCuenta, textvariable = self.boxEmail_var)
        self.boxEmail.place(x=120, y=165, width=180, height=25)

        Label(self.windowSubmenuGUModificarCuenta, text = "Tipo usuario:").place(x=5, y=195)
        self.comboTipoUsuario = ttk.Combobox(self.windowSubmenuGUModificarCuenta, state = "readonly", values = self.resultTipoUser)
        self.comboTipoUsuario.place(x=120, y=195, width=180, height=25)

        Label(self.windowSubmenuGUModificarCuenta, text = "Cámara:").place(x=5, y=225)
        self.comboCamara = ttk.Combobox(self.windowSubmenuGUModificarCuenta, state = "readonly", values = self.resultCamara)
        self.comboCamara.place(x=120, y=225, width=180, height=25)

        
        #COLUMNA DE BOTONES
        self.buttonModificar = Button(self.windowSubmenuGUModificarCuenta, text = "Modificar", command = self.modificarUsuario)
        self.buttonModificar.place(x=120, y=265, width=80, height=30)

        self.buttonRegresar  = Button(self.windowSubmenuGUModificarCuenta, text = "Regresar", command = lambda : GestionarUsuario(self.windowSubmenuGUModificarCuenta.withdraw()))
        self.buttonRegresar.place(x=220, y=265, width=80, height=30)

        self.idUsuario_var = IntVar()

    def modificarUsuario(self):
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboCamara.get() == "Elige una opción":
            return messagebox.showwarning("Modificar Usuario","Error, ningun campo puede quedar vacio")

        self.c.execute("SELECT * FROM Usuario WHERE correo = ?", (self.valor,))
        elUsuario=self.c.fetchall()
        
        for usuario in elUsuario:
            self.idUsuario_var.set(usuario[0])
        
        self.datos = self.comboCamara.get(), self.boxName.get(), self.boxLastname.get(), self.boxPassword.get(), self.boxEmail.get(), self.comboTipoUsuario.get(), self.idUsuario_var.get()
        self.c.execute("UPDATE Usuario SET  id_camara = ?, nombre = ?, apellido_p = ?, password = ?, correo = ?, tipoUsuario = ? WHERE idUsuario = ?", (self.datos))  
        self.db.commit()

        self.comboUser.set("Elige una opción")
        self.boxName.delete(0, 'end')
        self.boxLastname.delete(0, 'end')
        self.boxPassword.delete(0, 'end')
        self.boxEmail.delete(0, 'end')
        self.comboTipoUsuario.set("Elige una opción")
        self.comboCamara.set("Elige una opción")
    
        messagebox.showinfo("Modificar Usuario","Registro actualizado con éxito")


    def buscar(self):
        if self.comboUser.get() == "Elige una opción":
                return messagebox.showwarning("Modificar Usuario","Error, selecciona un usuario")

        self.valor = self.comboUser.get()

        self.c.execute("SELECT * FROM Usuario WHERE correo = ?", (self.valor,))
        elUsuario=self.c.fetchall()
            
        for usuario in elUsuario:
            
            self.idUsuario_var.set(usuario[0])
            self.comboCamara.set(usuario[1])
            self.boxName_var.set(usuario[2])
            self.boxLastname_var.set(usuario[3])
            self.boxPassword_var.set(usuario[4])
            self.boxEmail_var.set(usuario[5])
            self.comboTipoUsuario.set(usuario[6])
            
        """    
        print( self.boxName_var.get(), self.boxLastname_var.get(), 
        self.boxPassword_var.get(),self.boxEmail_var.get(),
        self.comboTipoUsuario.get(),self.comboCamara.get(),self.idUsuario_var.get())"""

        self.db.commit()


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class ReportePlacas():

    ################ ADMINISTRADOR – REPORTE DE PLACAS ###############  
    def __init__(self, args):
        self.windowSubmenuReportePlacas = Tk()
        self.windowSubmenuReportePlacas.geometry("350x200+500+250")
        self.windowSubmenuReportePlacas.title("Reporte de Placas")
        Label(self.windowSubmenuReportePlacas, text = "Reporte de Placas" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE BOTONES
        Button(self.windowSubmenuReportePlacas, text = "Obtener Reporte de Alertas", command = lambda : ObtenerReporteAlerta(self.windowSubmenuReportePlacas.withdraw())).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        Button(self.windowSubmenuReportePlacas, text = "Generar Reporte de Busqueda",  command = lambda : GenerarReporteBusqueda(self.windowSubmenuReportePlacas.withdraw())).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        Button(self.windowSubmenuReportePlacas, text = "Regresar", command = lambda : Administrador(self.windowSubmenuReportePlacas.withdraw())).place(x=260, y=160, width=80, height=30)


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################


class GenerarReporteBusqueda:

    ################ ADMINISTRADOR – REPORTE DE PLACAS – GENERAR REPORTE ###############
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

        #Lista para guardar los valores de los colores
        self.listaColores = ['Amarillo', 'Azul', 'Blanco', 'Cafe', 'Dorado', 'Gris',   
                             'Morado', 'Naranja', 'Negro', 'Rojo', 'Rosa', 'Verde', 'Vino']

        self.windowSubmenuRPGenerarReporte = Toplevel()
        self.windowSubmenuRPGenerarReporte.geometry("350x300+500+250")
        self.windowSubmenuRPGenerarReporte.title("Reporte de Placas/Generar Reporte")
        Label(self.windowSubmenuRPGenerarReporte, text = "Generar Reporte Busqueda" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE LABES, BOXES
        Label(self.windowSubmenuRPGenerarReporte, text = "Placa:" ).place(x=5, y=45)
        self.boxPlate_var = StringVar()
        self.boxPlate = Entry(self.windowSubmenuRPGenerarReporte, textvariable = self.boxPlate_var)
        self.boxPlate.place(x=105, y=45, width=180, height=25)

        Label(self.windowSubmenuRPGenerarReporte, text = "Marca" ).place(x=5, y=75)
        self.comboMarca = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=105, y=75, width=180, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuRPGenerarReporte, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=120, y=105, width=140, height=30)

        Label(self.windowSubmenuRPGenerarReporte, text = "Modelo" ).place(x=5, y=145)
        self.comboModelo = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=105, y=145, width=180, height=25)

        Label(self.windowSubmenuRPGenerarReporte, text = "Color" ).place(x=5, y=175)
        self.comboColor = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=105, y=175, width=180, height=25)

        #COLUMNA DE BOTONES
        self.buttonAceptar = Button(self.windowSubmenuRPGenerarReporte, text = "Aceptar", command = self.generarReporteBusqueda)
        self.buttonAceptar.place(x=105, y=220,  width=80, height=30)
        self.buttonRegresar = Button(self.windowSubmenuRPGenerarReporte, text = "Regresar", command = lambda : ReportePlacas(self.windowSubmenuRPGenerarReporte.withdraw()))
        self.buttonRegresar.place(x=200, y=220, width=80, height=30)

    def generarReporteBusqueda(self):

        if self.boxPlate.get() == "" or len(self.boxPlate.get()) > 9 or len(self.boxPlate.get()) < 7:
            if self.boxPlate.get() == "":
                return messagebox.showerror("Genear Reporte","Error, campo Placa no puede ir vacio")
            elif len(self.boxPlate.get()) > 9:
                return messagebox.showerror("Genear Reporte","Error, campo Placa excede caracteres permitidos")
            else:
                return messagebox.showerror("Genear Reporte","Error, campo Placa debe tener al menos 7 caracteres")
        elif self.comboMarca.get() == "Marca":
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

        messagebox.showinfo("Genear Reporte","Reporte de busqueda generado con éxito")

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

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

#SE INVOCA TANTPO POR ADMIN COMO POR USER, REALIZAR LÓGICA PARA CADA TIPO DE USUARIO
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
        self.windowSubmenuRPObtenerReporteAlerta.geometry("350x400+500+250")
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
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar", command = lambda : ReportePlacas(self.windowSubmenuRPObtenerReporteAlerta.withdraw()))
        self.buttonRegresar.place(x=200, y=250, width=100, height=30)


    def buscaReporteAlerta(self):
        self.textReporteGenerado.delete('1.0', tk.END)
        
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")
        #else:
        #    print(self.comboPlaca.get())
        
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file)
            
            for profile in profiles:
                if profile["Placa"] == self.comboPlaca.get():
                    profile1 = json.dumps(profile, indent=4, sort_keys=False)#Imprime bonito el JSON
                    self.textReporteGenerado.insert('1.0', profile1)#inserta valor en el widget text
            
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")
        #self.comboPlaca.set("Placa")

    def obtieneReporteAlerta(self):
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        file = open(f"./ObtenerReporteGuardados/{self.comboPlaca.get()}.txt", "w")
        file.write(f"{self.datosGuardarTxt}")
        #file.close()
        self.textReporteGenerado.delete('1.0', tk.END)
        return messagebox.showinfo("Guardar Reporte","Registro guardado con éxito")

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class ObtenerReporteAlertaUsuario:
    
    ################ ADMINISTRADOR – REPORTE DE PLACAS – OBTENER REPORTE ###############
    def __init__(self, args):
        self.listaPlacas = []
        with open('ReporteAlerta.json', 'r') as file:
            placasJson = json.load(file)
            for self.placaJson in placasJson:
                self.listaPlacas.append(self.placaJson["Placa"])
            self.listaPlacas.sort()
            

        self.windowSubmenuRPObtenerReporteAlerta = Toplevel()
        self.windowSubmenuRPObtenerReporteAlerta.geometry("350x400+500+250")
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
        self.buttonGuardar.place(x=50, y=250, width=80, height=30) #AQUI PORNER UN MENSAJE DE SE GUARDO CORRECTAMENTE,
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar", command = lambda : User(self.windowSubmenuRPObtenerReporteAlerta.withdraw())).place(x=250, y=360, width=80, height=30)
        self.buttonRegresar.place(x=200, y=250, width=100, height=30)

    def buscaReporteAlerta(self):
        self.textReporteGenerado.delete('1.0', tk.END)
        
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")
        #else:
        #    print(self.comboPlaca.get())
        
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file)
            
            for profile in profiles:
                if profile["Placa"] == self.comboPlaca.get():
                    profile1 = json.dumps(profile, indent=4, sort_keys=False)#Imprime bonito el JSON
                    self.textReporteGenerado.insert('1.0', profile1)#inserta valor en el widget text
            
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")
        #self.comboPlaca.set("Placa")

    def obtieneReporteAlerta(self):
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        file = open(f"./ObtenerReporteGuardados/{self.comboPlaca.get()}.txt", "w")
        file.write(f"{self.datosGuardarTxt}")
        #file.close()
        self.textReporteGenerado.delete('1.0', tk.END)
        return messagebox.showinfo("Guardar Reporte","Registro guardado con éxito")

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

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

        self.windowSubmenuMonitoreaCamara = Toplevel()
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
        self.buttonRegresar = Button(self.windowSubmenuMonitoreaCamara, text = "Regresar", command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        self.buttonRegresar.place(x=10, y=420, width=160, height=30)
        
        #self.windowSubmenuMonitoreaCamara.mainloop()

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

        self.camara.set("Elige una opción")

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
        


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class GenerarReporteAlerta:
    pass


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class VisualizarReporteAlerta:
    
    
    ################ MENÚ USUARIO – MONITOREAR CÁMARA – VISUALIZAR ALERTA ###############
    def visualizarAlerta(self, args):
        self.windowSubmenuVisualiza = Tk()
        self.windowSubmenuVisualiza.geometry("500x350+500+250")
        self.windowSubmenuVisualiza.title("Monitorear Cámara/Visualizar Alerta")
        Label(self.windowSubmenuVisualiza, text = "Visualizar Alerta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        
        #COLUMNA DE ETIQUETAS
        Label(self.windowSubmenuVisualiza, text = "Placa" ).place(x=5, y=45)
        Label(self.windowSubmenuVisualiza, text = "Modelo" ).place(x=5, y=75)
        Label(self.windowSubmenuVisualiza, text = "Color" ).place(x=5, y=105)

        #COLUMNA DE BOTONES
        Button(self.windowSubmenuVisualiza, text = "Regresar", command = lambda : MonitoreaCamara.monitorearCamara (self, self.windowSubmenuVisualiza.withdraw())).place(x=200, y=300, width=100, height=30)
        #windowSubmenuVisualiza. 

    def muestraDatosAlerta():
        pass
