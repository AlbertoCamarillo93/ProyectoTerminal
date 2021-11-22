import json
import os
import cv2
import random
import config
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

        #Bloque de botones
        self.buttonLogin = Button (self.windowLogin, text = "Login", command = self.login).pack()
        self.buttonExit = Button (self.windowLogin, text = "Salir", command = self.exit).pack()

        self.windowLogin.mainloop() #EJECUTA LA VENTANA PRINCIPAL


    #FUNCIÓN BOTÓN DE LOGEO
    def login(self):
        # Connect to database
        self.db = sqlite3.connect('proyecto_placas.db')
        self.c = self.db.cursor()
        
        #Query que selecciona al usuario y correo ingresado de la BD
        self.c.execute("SELECT * FROM Usuario WHERE correo=? AND password=?", (self.boxEmail.get(), self.boxPassword.get()))        
        row = self.c.fetchall() 

        self.obtieneVariablesGlobales()
        
        #Condicional que verifica tipo de usuario para enviarlo al menú correspondiente
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

    #Cierra la ventana
    def exit(self):
        self.windowLogin.destroy()

    def obtieneVariablesGlobales(self):

        self.c1 = self.db.cursor()
        #Query que selecciona toda la información del correo seleccionado por el usuario para modificar
        self.c1.execute("SELECT * FROM Usuario WHERE correo = ?", (self.boxEmail.get(),))
        elUsuario=self.c1.fetchall()
            
        #Recorre los valores del usuario para insertarle su nuevo valor en la posición que le corresponde
        for usuario in elUsuario:
            
            config.id_usuario = usuario[0]
            config.camara = usuario[1]
            config.nombre = usuario[2]
            config.apellido = usuario[3]
            config.contacto_usuario = usuario[5]
            
        self.db.commit()
        #print(config.camara, type(config.camara))      
        return config.id_usuario, config.camara, config.nombre, config.apellido, config.contacto_usuario

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class Administrador():

    def __init__(self, args):
        self.windowMenuAdmin = Toplevel()
        self.windowMenuAdmin.geometry("350x200+500+250")
        self.windowMenuAdmin.title("Menu Administrador")
        labeltitulo = Label(self.windowMenuAdmin, text = "Menu Administrador" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        
        #COLUMNA DE ETIQUETAS
        self.labelIdUsuario = Label(self.windowMenuAdmin, text = f"ID_Usuario \n{config.id_usuario}")
        self.labelIdUsuario.place(x=25, y=45)
        self.labelNombre =Label(self.windowMenuAdmin, text = f"Nombre \n{config.nombre} {config.apellido}" )
        self.labelNombre.place(x=15, y=80)
        self.labelDatosContacto = Label(self.windowMenuAdmin, text = f"Datos Contacto \n{config.contacto_usuario}" )
        self.labelDatosContacto.place(x=15, y=120)

        #COLUMNA DE BOTONES
        self.buttonGestionarUsuario = Button(self.windowMenuAdmin, text = "Gestión de usuarios", command = lambda : GestionarUsuario(self.windowMenuAdmin.withdraw()))
        self.buttonGestionarUsuario.place(x=200, y=45, width=120, height=30)

        self.buttonReportePlacas = Button(self.windowMenuAdmin, text = "Reporte de placas", command = lambda : ReportePlacas(self.windowMenuAdmin.withdraw()))
        self.buttonReportePlacas.place(x=200, y=90, width=120, height=30) 

        self.buttonCerrarSesion = Button(self.windowMenuAdmin, text = "Cerrar Sesión", command = lambda : Login(self.windowMenuAdmin.withdraw()))
        self.buttonCerrarSesion.place(x=240, y=160, width=100, height=30)

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class User():
    
    def __init__(self, args):   
        #Login.prueba(self)
        self.windowMenuUser = Toplevel()
        self.windowMenuUser.geometry("400x200+500+250")
        self.windowMenuUser.title("Menu Usuario")
        labeltitulo = Label(self.windowMenuUser, text = "Menu Usuario" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        
        #COLUMNA DE ETIQUETAS
        self.labelIdUsuario = Label(self.windowMenuUser, text = f"ID_Usuario \n{config.id_usuario}" )
        self.labelIdUsuario.place(x=25, y=45)
        self.labelNombre = Label(self.windowMenuUser, text = f"Nombre \n{config.nombre} {config.apellido}" )
        self.labelNombre.place(x=25, y=80)
        self.labelIdCamara = Label(self.windowMenuUser, text = f"Cámara \n {config.camara}" )
        self.labelIdCamara.place(x=25, y=120)
        self.labelDatosContacto = Label(self.windowMenuUser, text = f"Datos Contacto \n{config.contacto_usuario}" )
        self.labelDatosContacto.place(x=15, y=150)

        #COLUMNA DE BOTONES
        self.buttonReporteAlerta = Button(self.windowMenuUser, text = "Obtener Reporte de Alertas", command = lambda : ObtenerReporteAlertaUsuario(self.windowMenuUser.withdraw()))
        self.buttonReporteAlerta.place(x=200, y=45, width=180, height=30) 

        self.buttonMonitorearCamara = Button(self.windowMenuUser, text = "Monitorear Cámara", command = lambda : MonitoreaCamara(self.windowMenuUser.withdraw()))
        self.buttonMonitorearCamara.place(x=200, y=90, width=180, height=30)

        self.buttonCerrarSesion = Button(self.windowMenuUser, text = "Cerrar Sesión", command = lambda : Login(self.windowMenuUser.withdraw()))
        self.buttonCerrarSesion.place(x=200, y=135, width=180, height=30)

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class GestionarUsuario():
    
    def __init__(self, args):
        self.windowSubmenuGestionUsuarios = Tk()
        self.windowSubmenuGestionUsuarios.geometry("350x200+500+250")
        self.windowSubmenuGestionUsuarios.title("Gestión Usuarios")

        labeltitulo = Label( self.windowSubmenuGestionUsuarios, text = "Gestión Usuarios" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)

        #COLUMNA DE BOTONES
        self.buttonCrear = Button( self.windowSubmenuGestionUsuarios, text = "Crear Cuenta", command = lambda : GestionarUsuarioCrear(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonCrear.pack(padx= 5, pady = 5, ipadx = 15, ipady = 5)

        self.buttonModificar = Button( self.windowSubmenuGestionUsuarios, text = "Modificar Cuenta", command = lambda : GestionarUsuarioModificar(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonModificar.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5) 

        self.buttonEliminar = Button( self.windowSubmenuGestionUsuarios, text = "Eliminar Cuenta",  command =  lambda : GestionarUsuarioElimina(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonEliminar.pack(padx= 5, pady = 5, ipadx = 10, ipady = 5)

        self.buttonregresar = Button( self.windowSubmenuGestionUsuarios, text = "Regresar", command = lambda : Administrador(self.windowSubmenuGestionUsuarios.withdraw()))
        self.buttonregresar.place(x=260, y=160, width=80, height=30) 

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class GestionarUsuarioElimina():

    def __init__(self, args):
        #Conecta a la BD
        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c = self.db.cursor()
        self.c1 = self.db.cursor()

        #Consulta los correos de la BD y los ordena
        self.c.execute("SELECT correo FROM Usuario ORDER BY correo ASC ")   

        #Se crea lista y se recorre agregando los datos obtenidos en el query
        self.result = []
        for row in self.c.fetchall():
            self.result.append(row[0])

        #Valores primarios de la ventana
        self.windowSubmenuGUEliminarCuenta = Tk()
        self.windowSubmenuGUEliminarCuenta.geometry("350x150+500+250")
        self.windowSubmenuGUEliminarCuenta.title("Gestión Usuarios/Eliminar Cuenta")
        labeltitulo = Label(self.windowSubmenuGUEliminarCuenta, text = "Eliminar Cuenta" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)

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
        #Condicional que verifica que se haya seleccionado un usuario
        if self.comboEliminar.get() == "Elige una opción":
                return messagebox.showwarning("Eliminar Usuario","Error, selecciona un usuario")

        #Query que eliminar el usuario seleccionado por el usuario
        self.c1.execute("DELETE FROM Usuario WHERE correo = ?", (self.comboEliminar.get(),))                 
        
        #Bloque que elimina del combobox la opción eliminada por el usuario y limpia el combobox
        n = 0
        for row in self.result:
            if self.comboEliminar.get() == row:
                del self.result[n]
            n+= 1
        self.comboEliminar ["values"]= self.result
        self.comboEliminar.set("Elige una opción")

        self.db.commit()
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
        labeltitulo = Label(self.windowSubmenuGUCrearCuenta, text = "Crear Cuenta" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)

        #COLUMNA DE LABES Y BOXES
        Label(self.windowSubmenuGUCrearCuenta, text = "Nombre:" ).place(x=5, y=45)
        self.boxName = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxName.place(x=105, y=45, width=180, height=25)

        Label(self.windowSubmenuGUCrearCuenta, text = "Apellido Paterno:" ).place(x=5, y=75)
        self.boxLastname = Entry(self.windowSubmenuGUCrearCuenta)
        self.boxLastname.place(x=105, y=75,  width=180, height=25)

        Label(self.windowSubmenuGUCrearCuenta, text = "Contraseña" ).place(x=5, y=105)
        self.boxPassword = Entry(self.windowSubmenuGUCrearCuenta,  show = "*")
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
        
        #Condiciones que no debe haber para poder crear un usuario
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboAsignarCamara.get() == "Elige una opción":
            return messagebox.showwarning("Crear Usuario","Error, ningun campo puede quedar vacio")
        elif len(self.boxPassword.get()) < 4:
            return messagebox.showwarning("Crear Usuario","Error, la contraseña debe tener al menos 4 digitos")
        elif self.boxEmail.get().find('@') == -1:
            return messagebox.showwarning("Crear Usuario","Error, no es un correo valido")
        elif self.boxEmail.get().find('.com') == -1:
            return messagebox.showwarning("Crear Usuario","Error, no es un correo valido")
        
        #Crea conexión a la BD y realiza consulta de todos los correos de los usuarios
        self.c4 = self.db.cursor()
        self.c4.execute("SELECT correo FROM Usuario") 
        
        #Crea una lista y luego  almacena en ella el valor del email dado por el usuario
        self.listaCorreoSeleccionado = []
        self.listaCorreoSeleccionado.append(self.boxEmail.get())
       
        #Crea una lista y luego  almacena en ella el valor de todos los correos de la BD
        self.listaCorreos = []
        for row in self.c4.fetchall():
            self.listaCorreos.append(row[0])
        
        n=0
        #Ciclo para verificar si el correo esta dentro o no de la BD
        for i in self.listaCorreos:
            n+=1
            if  self.listaCorreoSeleccionado[0] not in self.listaCorreos   :
                self.listaCorreos.append(self.listaCorreoSeleccionado[0])
                break  
            elif self.listaCorreos[n] == self.listaCorreoSeleccionado[0]:
                return messagebox.showwarning("Crear Usuario","Error, el correo ya existe")
            
        #Crea conexión a la BD y realiza un insert con los valores dados por el usuario
        self.c = self.db.cursor()
        self.datos = self.comboAsignarCamara.get(), self.boxName.get().capitalize(),self.boxLastname.get().capitalize(),self.boxPassword.get(),self.boxEmail.get(),self.comboTipoUsuario.get()
        self.c.execute("INSERT INTO Usuario VALUES(NULL,?,?,?,?,?,?)", (self.datos))  
            
        self.db.commit()

        #Limpia widgets de la ventana
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

        #Conexiones a BD
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

        #Definiendo valores primarios de la ventana
        self.windowSubmenuGUModificarCuenta = Toplevel()
        self.windowSubmenuGUModificarCuenta.geometry("350x320+500+250")
        self.windowSubmenuGUModificarCuenta.title("Gestión Usuarios/Modificar Cuenta")
        labeltitulo = Label(self.windowSubmenuGUModificarCuenta, text = "Modificar Cuenta" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)

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

        Label(self.windowSubmenuGUModificarCuenta, text = "Contraseña").place(x=5, y=135)
        self.boxPassword_var = StringVar()
        self.boxPassword = Entry(self.windowSubmenuGUModificarCuenta, textvariable = self.boxPassword_var, show = "*")
        self.boxPassword.place(x=120, y=135,  width=180, height=25)
        
        Label(self.windowSubmenuGUModificarCuenta, text = "Correo:").place(x=5, y=165)
        self.boxEmail_var = StringVar()
        self.boxEmail = Entry(self.windowSubmenuGUModificarCuenta, state = "readonly", textvariable = self.boxEmail_var)
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
        #Verifica que no esten en blanco los widgets Entry, así como en el email, se este registrando uno valido
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboCamara.get() == "Elige una opción":
            return messagebox.showwarning("Modificar Usuario","Error, ningun campo puede quedar vacio")
        elif len(self.boxPassword.get()) < 4:
            return messagebox.showwarning("Modificar Usuario","Error, la contraseña debe tener al menos 4 digitos")
        elif self.boxEmail.get().find('@') == -1:
            return messagebox.showwarning("Modificar Usuario","Error, no es un correo valido")
        elif self.boxEmail.get().find('.com') == -1:
            return messagebox.showwarning("Modificar Usuario","Error, no es un correo valido")
       
        #Realiza el update con los datos dentro de los Entry
        self.datos = self.comboCamara.get(), self.boxName.get(), self.boxLastname.get(), self.boxPassword.get(), self.boxEmail.get(), self.comboTipoUsuario.get(), self.idUsuario_var.get()
        self.c.execute("UPDATE Usuario SET  id_camara = ?, nombre = ?, apellido_p = ?, password = ?, correo = ?, tipoUsuario = ? WHERE idUsuario = ?", (self.datos))  
        
        #Limpia los campos al finalizar la transacción
        self.comboUser.set("Elige una opción")
        self.boxName.delete(0, 'end')
        self.boxLastname.delete(0, 'end')
        self.boxPassword.delete(0, 'end')
        self.boxEmail.delete(0, 'end')
        self.comboTipoUsuario.set("Elige una opción")
        self.comboCamara.set("Elige una opción")

        #Limpia el combobox para seleccionar el correo del usuario a modificar
        n = 0
        for row in self.result:
            if self.comboUser.get() == row:
                del self.result[n]
            n+= 1
        self.comboUser ["values"]= self.result
        self.comboUser.set("Elige una opción")

        self.db.commit()
        messagebox.showinfo("Modificar Usuario","Registro actualizado con éxito")


    def buscar(self):
        #Verifica condición de que se eligió un usuario para su modificación
        if self.comboUser.get() == "Elige una opción":
                return messagebox.showwarning("Modificar Usuario","Error, selecciona un usuario")

        #Query que selecciona toda la información del correo seleccionado por el usuario para modificar
        self.c.execute("SELECT * FROM Usuario WHERE correo = ?", (self.comboUser.get(),))
        elUsuario=self.c.fetchall()
            
        #Recorre los valores del usuario para insertarle su nuevo valor en la posición que le corresponde
        for usuario in elUsuario:
            
            self.idUsuario_var.set(usuario[0])
            self.comboCamara.set(usuario[1])
            self.boxName_var.set(usuario[2])
            self.boxLastname_var.set(usuario[3])
            self.boxPassword_var.set(usuario[4])
            self.boxEmail_var.set(usuario[5])
            self.comboTipoUsuario.set(usuario[6])
            
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
        labeltitulo = Label(self.windowSubmenuReportePlacas, text = "Reporte de Placas" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)

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

        #Lista con los valores de los colores
        self.listaColores = ['Amarillo', 'Azul', 'Blanco', 'Cafe', 'Dorado', 'Gris',   
                             'Morado', 'Naranja', 'Negro', 'Rojo', 'Rosa', 'Verde', 'Vino']
        
        #Lista con los valores del abecedario permitidos por las placas
        self.listaAbecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', 'Ñ','O',
                                'P','Q','R','S','T','U','V','W','X','Y','Z',
                                'a','b','c','d','e','f','g','h','i','j','k','l','m','n', 'ñ','o',
                                'p','q','r','s','t','u','v','w','x','y','z']
        
        #Lista con los valores los numeros permitidos por las placas
        self.listaNumeros = ['0','1','2','3','4','5','6','7','8','9']

        #Configuraciones básicas de la ventana
        self.windowSubmenuRPGenerarReporte = Toplevel()
        self.windowSubmenuRPGenerarReporte.geometry("350x300+500+250")
        self.windowSubmenuRPGenerarReporte.title("Reporte de Placas/Generar Reporte")
        labeltitulo = Label(self.windowSubmenuRPGenerarReporte, text = "Generar Reporte Busqueda" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        #RADIOBUTTON
        self.opcion = IntVar()
        self.buttonCDMX = Radiobutton(self.windowSubmenuRPGenerarReporte, text="Ciudad de México", variable= self.opcion, value=1, command= self.selectRadioButton)
        self.buttonCDMX.place(x=20, y=45)
        self.buttonEdoMex = Radiobutton(self.windowSubmenuRPGenerarReporte, text="Estado de México", variable= self.opcion, value=2, command= self.selectRadioButton)
        self.buttonEdoMex.place(x=160, y=45)

        #BLOQUE DE LABELS, BOXES
        #Placa
        Label(self.windowSubmenuRPGenerarReporte, text = "Placa:" ).place(x=5, y=70)
        self.boxPlate_var = StringVar()
        self.boxPlate = Entry(self.windowSubmenuRPGenerarReporte, textvariable = self.boxPlate_var)
        self.boxPlate.place(x=105, y=70, width=180, height=25)

        #Marca
        Label(self.windowSubmenuRPGenerarReporte, text = "Marca:" ).place(x=5, y=105)
        self.comboMarca = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=105, y=105, width=180, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuRPGenerarReporte, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=120, y=140, width=140, height=30)

        #Modelo
        Label(self.windowSubmenuRPGenerarReporte, text = "Modelo:" ).place(x=5, y=180)
        self.comboModelo = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=105, y=180, width=180, height=25)

        #Color
        Label(self.windowSubmenuRPGenerarReporte, text = "Color:" ).place(x=5, y=215)
        self.comboColor = ttk.Combobox(self.windowSubmenuRPGenerarReporte,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=105, y=215, width=180, height=25)

        #BLOQUE DE BOTONES
        self.buttonAceptar = Button(self.windowSubmenuRPGenerarReporte, text = "Aceptar", command = self.generarReporteBusqueda)
        self.buttonAceptar.place(x=105, y=250,  width=80, height=30)
        self.buttonRegresar = Button(self.windowSubmenuRPGenerarReporte, text = "Regresar", command = lambda : ReportePlacas(self.windowSubmenuRPGenerarReporte.withdraw()))
        self.buttonRegresar.place(x=200, y=250, width=80, height=30)

    def generarReporteBusqueda(self):
        
        #Verifica longitud del Entry boxPlate, para saber si es valido o no
        if self.opcion.get() == False:
            return messagebox.showerror("Genear Reporte","Error, selecciona un tipo de placa")
        elif self.boxPlate.get() == "":
            return messagebox.showerror("Genear Reporte","Error, campo Placa no puede ir vacio")

        #Placa CDMX, verifica valor valido para placas de la CDMX
        if self.opcion.get() == 1:
            if len(self.boxPlate.get()) == 7:
                for indice in range(len(self.boxPlate.get())):
                    caracter = '-'
                    if self.boxPlate.get()[0] not in self.listaNumeros and self.boxPlate.get()[0] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif self.boxPlate.get()[1] not in self.listaNumeros or self.boxPlate.get()[2] not in self.listaNumeros:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif caracter != self.boxPlate.get()[3]:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif self.boxPlate.get()[4] not in self.listaAbecedario or self.boxPlate.get()[5] not in self.listaAbecedario or self.boxPlate.get()[6] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
            else:
                return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
        
        #Placa EdoMex, verifica valor valido para placas del EdoMex
        if self.opcion.get() == 2:
            if len(self.boxPlate.get()) == 9:
                for indice in range(len(self.boxPlate.get())):
                    caracter = '-'
                    if caracter != self.boxPlate.get()[3] or caracter != self.boxPlate.get()[6]:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
                    elif self.boxPlate.get()[0] not in self.listaAbecedario or self.boxPlate.get()[1] not in self.listaAbecedario or self.boxPlate.get()[2] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
                    elif self.boxPlate.get()[4] not in self.listaNumeros or self.boxPlate.get()[5] not in self.listaNumeros or self.boxPlate.get()[7] not in self.listaNumeros or self.boxPlate.get()[8] not in self.listaNumeros:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
            else:
                return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
        
        #Verifica que campo Marca, modelo y color no queden vacios
        if self.comboMarca.get() == "Marca":
            return messagebox.showerror("Genear Reporte","Error, selecciona una marca")
        elif self.comboModelo.get() == "Modelo":
            return messagebox.showerror("Genear Reporte","Error, selecciona un modelo")
        elif self.comboColor.get() == "Color":
            return messagebox.showerror("Genear Reporte","Error, selecciona un color")

        #Valores que toma el diccionario para insertarlos en el archivo json
        data_dict =  {
            "Placa"  : f"{self.boxPlate.get().upper()}",
            "Marca"  : f"{self.comboMarca.get()}",
            "Modelo" : f"{self.comboModelo.get()}",
            "Color"  : f"{self.comboColor.get()}"
            }

        #Bloque que lee, abre, y escribe en el archivo json los datos del diccionario
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
            # Crea el archivo en caso de no existir
            with open(fname, 'w') as outfile:
                array = []
                array.append(data_dict)
                json.dump(array, outfile)

        #Limpia los valores a los predeterminados al finalizar
        self.boxPlate.delete(0, 'end')
        self.comboMarca.set("Marca")
        self.comboModelo.set("Modelo")
        self.comboColor.set("Color")

        messagebox.showinfo("Genear Reporte","Reporte de busqueda generado con éxito")

    def obtenerModelo(self):
        #Verifica que se elija una marca
        if self.comboMarca.get() == "Marca":
            return messagebox.showwarning("Genear Reporte","Error, selecciona una marca")

        self.valor = self.comboMarca.get()
        #Consulta la BD para traer de ella, los modelos correspondientes a la marca elegida
        self.c2.execute("SELECT Modelo FROM MarcaModelo WHERE Marca = ? ORDER BY Modelo ASC", (self.valor,))
        
        #Verifica si la lista esta vacia, si es así agrega los datos encontrados de la consulta
        if self.listaModelo == []:
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])
        #Sino esta vacia la borra y agrega los datos de la consulta
        else:
            del self.listaModelo [:]
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])

        self.db.commit
        #Limpia el combobox del modelo
        self.comboModelo ["values"]= self.listaModelo
        self.comboModelo.set("Modelo")

    def selectRadioButton(self):
        #Verifica el radioButton seleccionado y devuelve en el widget entry el formato de placa según sea el caso
        if self.opcion.get() == 1:
            self.boxPlate_var.set("A00-AAA / 000-AAA")
        else:
            self.boxPlate_var.set("AAA-00-00")

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

#SE INVOCA TANTPO POR ADMIN COMO POR USER, REALIZAR LÓGICA PARA CADA TIPO DE USUARIO
class ObtenerReporteAlerta:
    
    ################ ADMINISTRADOR – REPORTE DE PLACAS – OBTENER REPORTE ###############
    def __init__(self, args):

        #Crea lista y abre y lee el archivo donde se almacenan los reportes de alerta
        self.listaPlacas = []
        with open('ReporteAlerta.json', 'r') as file:
            #Convierte los datos Json en datos equivalentes a Python
            placasJson = json.load(file)
            #Ciclo que agrega a la lista cada valor del archivo json
            for self.placaJson in placasJson:
                self.listaPlacas.append(self.placaJson["Placa"])
            #Ordena los datos de la lista
            self.listaPlacas.sort()
            
        #Datos primarios de la ventana
        self.windowSubmenuRPObtenerReporteAlerta = Toplevel()
        #Centra ventana en la pantalla
        ancho_ventana = 350
        alto_ventana = 400
        x_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.windowSubmenuRPObtenerReporteAlerta.geometry(posicion)

        self.windowSubmenuRPObtenerReporteAlerta.title("Reporte de Placas/Obtener Reporte")
        labeltitulo = Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Obtener Reporte Alerta" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        #COLUMNA DE LABES, BOXES
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Ingresa la placa para obtener el reporte:" ).place(x=5, y=45)
       
        #Placa
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Placa:" ).place(x=5, y=75)
        self.comboPlaca = ttk.Combobox(self.windowSubmenuRPObtenerReporteAlerta,  state = "readonly")
        self.comboPlaca ["values"] = self.listaPlacas
        self.comboPlaca.set("Placa")
        self.comboPlaca.place(x=50, y=75, width=130, height=30)

        #Aceptar
        self.buttonAceptar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Aceptar", command = self.buscaReporteAlerta)
        self.buttonAceptar.place(x=200, y=75, width=80, height=30)
        
        #Texto del reporte
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "El reporte generado es:" ).place(x=5, y=110)
        self.textReporteGenerado = Text(self.windowSubmenuRPObtenerReporteAlerta, state = "normal")
        self.textReporteGenerado.place(x=5, y=140,  width=330, height=180)

        #COLUMNA DE BOTONES
        self.buttonGuardar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Guardar", command = self.guardaReporteAlerta)
        self.buttonGuardar.place(x=50, y=340, width=100, height=30)
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar", command = lambda : ReportePlacas(self.windowSubmenuRPObtenerReporteAlerta.withdraw()))
        self.buttonRegresar.place(x=200, y=340, width=100, height=30)

    def buscaReporteAlerta(self):
        #Limpia el widget Text cada que se va a ingresar nueva información
        self.textReporteGenerado.delete('1.0', tk.END)
        
        #Condional que verifica que se haya seleccionado una opción
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")

        #Conexión a BD
        self.db = sqlite3.connect('proyecto_placas.db')
        self.c1 = self.db.cursor()       

        #Abre el archivo donde se almacenan los reportes de alerta y lo lee
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file) #Convierte los datos Json en datos equivalentes a Python
            
            #Ciclo que recorre los valores del json en busca de coincidencia con el valor elegido en el combobox
            for data in profiles:
                if data["Placa"] == self.comboPlaca.get():
                    self.camaraSalvar = data['Camara']
                    profile1 = json.dumps(data, indent=4, sort_keys=False)#Imprime los datos en formato JSON
                    self.textReporteGenerado.insert('1.0', profile1)#Inserta el valor completo de la placa en el widget text

            #Busca que el nombre de la placa en el Json coincida con el valor elegido, lo almacena en una variable para su posterior uso
        for plate in profiles:
            if plate['Placa'] == self.comboPlaca.get():
                self.placaSalvar = plate['Placa']
        
        
        #Selecciona valores de la tabla de Camara 
        self.c1.execute("SELECT idCamara, calle, colonia, delegacion FROM Camara WHERE idCamara = ?", (self.camaraSalvar,)) 
        
        #Almacena en lista datosJson los valores de la consulta a la BD
        self.datosJson = []
        for row in self.c1.fetchall():
            self.datosJson.append(row)
            
        #Almacena los valores del Json
        idCamara = self.datosJson[0][0]
        calle = self.datosJson[0][1]
        colonia = self.datosJson[0][2]
        alcaldia = self.datosJson[0][3]

        #Agrega los datos de la camara en la BD en el widget de Text 
        self.textReporteGenerado.insert('1.0', f"idCamara: {idCamara}\nCalle: {calle}\nColonia: {colonia}\nAlcaldia: {alcaldia}\n")#inserta valor en el widget text

        #Almacena el valor obtenido en el widget
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")

    def guardaReporteAlerta(self):
        #Condicional que verifica si hay información dentro del widget Text
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        #Crea un archivo de escritura con el nombre de la placa seleccionada en el combobox
        file = open(f"./ObtenerReporteVisualizacion_Guardados/{self.placaSalvar}.txt", "w")
        #Escribe los datos obtenidos en el widget Text
        file.write(f"{self.datosGuardarTxt}")
        #Limpia el widget Text
        self.textReporteGenerado.delete('1.0', tk.END)

        #Limpia los valores del combobox de la placa
        self.comboPlaca ["values"]= self.listaPlacas
        self.comboPlaca.set("Placa")
        return messagebox.showinfo("Guardar Reporte","Registro guardado con éxito")

######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class ObtenerReporteAlertaUsuario:
    
    def __init__(self, args):

        #Crea lista y abre y lee el archivo donde se almacenan los reportes de alerta
        self.listaPlacas = []
        with open('ReporteAlerta.json', 'r') as file:
            #Convierte los datos Json en datos equivalentes a Python
            placasJson = json.load(file)
            #Ciclo que agrega a la lista cada valor del archivo json
            for self.placaJson in placasJson:
                self.listaPlacas.append(self.placaJson["Placa"])
            #Ordena los datos de la lista
            self.listaPlacas.sort()
            
        #Datos primarios de la ventana
        self.windowSubmenuRPObtenerReporteAlerta = Toplevel()
        #Centra ventana en la pantalla
        ancho_ventana = 350
        alto_ventana = 400
        x_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.windowSubmenuRPObtenerReporteAlerta.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.windowSubmenuRPObtenerReporteAlerta.geometry(posicion)

        self.windowSubmenuRPObtenerReporteAlerta.title("Reporte de Placas/Obtener Reporte")
        labeltitulo = Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Obtener Reporte Alerta" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        #COLUMNA DE LABES, BOXES
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Ingresa la placa para obtener el reporte:" ).place(x=5, y=45)
       
        #Placa
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "Placa:" ).place(x=5, y=75)
        self.comboPlaca = ttk.Combobox(self.windowSubmenuRPObtenerReporteAlerta,  state = "readonly")
        self.comboPlaca ["values"] = self.listaPlacas
        self.comboPlaca.set("Placa")
        self.comboPlaca.place(x=50, y=75, width=130, height=30)

        #Aceptar
        self.buttonAceptar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Aceptar", command = self.buscaReporteAlerta)
        self.buttonAceptar.place(x=200, y=75, width=80, height=30)
        
        #Texto del reporte
        Label(self.windowSubmenuRPObtenerReporteAlerta, text = "El reporte generado es:" ).place(x=5, y=110)
        self.textReporteGenerado = Text(self.windowSubmenuRPObtenerReporteAlerta, state = "normal")
        self.textReporteGenerado.place(x=5, y=140,  width=330, height=180)

        #COLUMNA DE BOTONES
        self.buttonGuardar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Guardar", command = self.guardaReporteAlerta)
        self.buttonGuardar.place(x=50, y=340, width=100, height=30)
        self.buttonRegresar = Button(self.windowSubmenuRPObtenerReporteAlerta, text = "Regresar", command = lambda : User(self.windowSubmenuRPObtenerReporteAlerta.withdraw()))
        self.buttonRegresar.place(x=200, y=340, width=100, height=30)

    def buscaReporteAlerta(self):
        #Limpia el widget Text cada que se va a ingresar nueva información
        self.textReporteGenerado.delete('1.0', tk.END)
        
        #Condional que verifica que se haya seleccionado una opción
        if self.comboPlaca.get() == "Placa":
            return messagebox.showwarning("Obtener Reporte","Error, selecciona una placa")

        #Conexión a BD
        self.db = sqlite3.connect('proyecto_placas.db')
        self.c1 = self.db.cursor()       

        #Abre el archivo donde se almacenan los reportes de alerta y lo lee
        with open('ReporteAlerta.json', 'r') as file:
            profiles = json.load(file) #Convierte los datos Json en datos equivalentes a Python
            
            #Ciclo que recorre los valores del json en busca de coincidencia con el valor elegido en el combobox
            for data in profiles:
                if data["Placa"] == self.comboPlaca.get():
                    self.camaraSalvar = data['Camara']
                    profile1 = json.dumps(data, indent=4, sort_keys=False)#Imprime los datos en formato JSON
                    self.textReporteGenerado.insert('1.0', profile1)#Inserta el valor completo de la placa en el widget text

            #Busca que el nombre de la placa en el Json coincida con el valor elegido, lo almacena en una variable para su posterior uso
        for plate in profiles:
            if plate['Placa'] == self.comboPlaca.get():
                self.placaSalvar = plate['Placa']
        
        
        #Selecciona valores de la tabla de Camara 
        self.c1.execute("SELECT idCamara, calle, colonia, delegacion FROM Camara WHERE idCamara = ?", (self.camaraSalvar,)) 
        
        #Almacena en lista datosJson los valores de la consulta a la BD
        self.datosJson = []
        for row in self.c1.fetchall():
            self.datosJson.append(row)
            
        #Almacena los valores del Json
        idCamara = self.datosJson[0][0]
        calle = self.datosJson[0][1]
        colonia = self.datosJson[0][2]
        alcaldia = self.datosJson[0][3]

        #Agrega los datos de la camara en la BD en el widget de Text 
        self.textReporteGenerado.insert('1.0', f"idCamara: {idCamara}\nCalle: {calle}\nColonia: {colonia}\nAlcaldia: {alcaldia}\n")#inserta valor en el widget text

        #Almacena el valor obtenido en el widget
        self.datosGuardarTxt = self.textReporteGenerado.get('1.0', tk.END+"-1c")

    def guardaReporteAlerta(self):
        #Condicional que verifica si hay información dentro del widget Text
        if self.textReporteGenerado.get('1.0', tk.END+"-1c") == "": #-1c significa que la posición está un carácter por delante de "end"
            return messagebox.showwarning("Guardar Reporte","No hay nada que guardar")

        #Crea un archivo de escritura con el nombre de la placa seleccionada en el combobox
        file = open(f"./ObtenerReporteVisualizacion_Guardados/{self.placaSalvar}.txt", "w")
        #Escribe los datos obtenidos en el widget Text
        file.write(f"{self.datosGuardarTxt}")
        #Limpia el widget Text
        self.textReporteGenerado.delete('1.0', tk.END)

        #Limpia los valores del combobox de la placa
        self.comboPlaca ["values"]= self.listaPlacas
        self.comboPlaca.set("Placa")
        return messagebox.showinfo("Guardar Reporte","Registro guardado con éxito")


######################################################################################################################################################        
######################################################################################################################################################
######################################################################################################################################################

class MonitoreaCamara:
    ################ MENÚ USUARIO – MONITOREAR CÁMARA ###############
    def __init__(self, args):

        #Conecta a la BD
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
        
        #Lista con los valores del abecedario permitidos por las placas
        self.listaAbecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N', 'Ñ','O',
                                'P','Q','R','S','T','U','V','W','X','Y','Z',
                                'a','b','c','d','e','f','g','h','i','j','k','l','m','n', 'ñ','o',
                                'p','q','r','s','t','u','v','w','x','y','z']
        
        #Lista con los valores los numeros permitidos por las placas
        self.listaNumeros = ['0','1','2','3','4','5','6','7','8','9']

        #Configuración básica de la ventana
        self.windowSubmenuMonitoreaCamara = Toplevel()
        #Centra la ventana a la mitad de la pantalla
        ancho_ventana = 850
        alto_ventana = 500
        x_ventana = self.windowSubmenuMonitoreaCamara.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.windowSubmenuMonitoreaCamara.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.windowSubmenuMonitoreaCamara.geometry(posicion)
        self.windowSubmenuMonitoreaCamara.title("Menu Usuario/Monitorear Cámara")
        labeltitulo = Label(self.windowSubmenuMonitoreaCamara, text = "Monitorear Cámara" )
        labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
        labeltitulo.config(font=16)
        
        #COLUMNA DE COMBOBOX   
        # Cámara 
        Label(self.windowSubmenuMonitoreaCamara, text = "Seleccionar Cámara:").place(x=5, y=40)
        self.camara = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly")
        self.camara.set(config.camara)
        self.camara.place(x=120, y=40, width=130, height=25)
        self.btnVisualizar = Button(self.windowSubmenuMonitoreaCamara, text="Visualizar video", command=self.visualizarVideo)
        self.btnVisualizar.place(x=260, y=40, width=100, height=25)

        #COLUMNA DE VALORES
        Label(self.windowSubmenuMonitoreaCamara, text = "Datos de la placa detectada" ).place(x=5, y=70)
        
        #RADIOBUTTON
        self.opcion = IntVar()
        self.buttonCDMX = Radiobutton(self.windowSubmenuMonitoreaCamara, text="Ciudad de México", variable= self.opcion, value=1, command= self.selectRadioButton)
        self.buttonCDMX.place(x=5, y=90)
        self.buttonEdoMex = Radiobutton(self.windowSubmenuMonitoreaCamara, text="Estado de México", variable= self.opcion, value=2, command= self.selectRadioButton)
        self.buttonEdoMex.place(x=5, y=110)

        #Placa
        Label(self.windowSubmenuMonitoreaCamara, text = "Placa" ).place(x=5, y=130)
        self.entryPlaca_var = StringVar()
        self.entryPlaca = Entry(self.windowSubmenuMonitoreaCamara, textvariable = self.entryPlaca_var)
        self.entryPlaca.place(x=5, y=150, width=160, height=25)

        #Marca
        Label(self.windowSubmenuMonitoreaCamara, text = "Marca" ).place(x=5, y=180)
        self.comboMarca = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=5, y=200, width=160, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuMonitoreaCamara, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=10, y=230, width=160, height=30)

        #Modelo
        Label(self.windowSubmenuMonitoreaCamara, text = "Modelo" ).place(x=5, y=270)
        self.comboModelo = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=5, y=290, width=160, height=25)

        #Color
        Label(self.windowSubmenuMonitoreaCamara, text = "Color" ).place(x=5, y=320)
        self.comboColor = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=5, y=340, width=160, height=25)

        #Video
        self.lblVideo = Label(self.windowSubmenuMonitoreaCamara, text = "" )
        self.lblVideo.place(x=185, y=105)

        #COLUMNA DE BOTONES
        self.buttonGenerar = Button(self.windowSubmenuMonitoreaCamara, text = "Generar Reporte de Alerta", command = self.generarReporteAlerta)
        self.buttonGenerar.place(x=10, y=380, width=160, height=30 )
        #self.buttonVisualizar = Button(self.windowSubmenuMonitoreaCamara, text = "Visualizar Alerta", command = lambda : VisualizarReporteAlerta.visualizarAlerta(self, self.windowSubmenuMonitoreaCamara.withdraw()))
        #self.buttonVisualizar.place(x=10, y=260, width=120, height=30)
        self.buttonLimpiar = Button(self.windowSubmenuMonitoreaCamara, text = "Limpiar", command = self.LimpiarWidgets)#, command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        self.buttonLimpiar.place(x=10, y=420, width=160, height=30)
        self.buttonRegresar = Button(self.windowSubmenuMonitoreaCamara, text = "Regresar", command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        self.buttonRegresar.place(x=10, y=460, width=160, height=30)

    def LimpiarWidgets(self):
        self.opcion.set(0)
        self.entryPlaca.delete(0, 'end')
        self.comboMarca.set("Marca")
        self.comboModelo.set("Modelo")
        self.comboColor.set("Color")

    def monitorearCamara(self):
        pass

    def generarReporteAlerta(self):

        #Verifica que button radio no este vacio ni el campo placa
        if self.opcion.get() == False:
            return messagebox.showerror("Genear Reporte","Error, selecciona un tipo de placa")
        elif self.entryPlaca.get() == "":
            return messagebox.showerror("Genear Reporte","Error, campo Placa no puede ir vacio")

        #Placa CDMX, verifica valor valido para placas de la CDMX
        if self.opcion.get() == 1:
            if len(self.entryPlaca.get()) == 7:
                for indice in range(len(self.entryPlaca.get())):
                    caracter = '-'
                    if self.entryPlaca.get()[0] not in self.listaNumeros and self.entryPlaca.get()[0] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif self.entryPlaca.get()[1] not in self.listaNumeros or self.entryPlaca.get()[2] not in self.listaNumeros:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif caracter != self.entryPlaca.get()[3]:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                    elif self.entryPlaca.get()[4] not in self.listaAbecedario or self.entryPlaca.get()[5] not in self.listaAbecedario or self.entryPlaca.get()[6] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
            else:
                return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con alguno de los siguientes formatos: \n A00-AAA \n 000-AAA")
                         
        #Placa EdoMex, verifica valor valido para placas del EdoMex
        if self.opcion.get() == 2:
            if len(self.entryPlaca.get()) == 9:
                for indice in range(len(self.entryPlaca.get())):
                    caracter = '-'
                    if caracter != self.entryPlaca.get()[3] or caracter != self.entryPlaca.get()[6]:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
                    elif self.entryPlaca.get()[0] not in self.listaAbecedario or self.entryPlaca.get()[1] not in self.listaAbecedario or self.entryPlaca.get()[2] not in self.listaAbecedario:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
                    elif self.entryPlaca.get()[4] not in self.listaNumeros or self.entryPlaca.get()[5] not in self.listaNumeros or self.entryPlaca.get()[7] not in self.listaNumeros or self.entryPlaca.get()[8] not in self.listaNumeros:
                        return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
            else:
                return messagebox.showerror("Genear Reporte","Error, Formato inválido, pruebe con el siguiente formato: \n AAA-00-00")
        
        #Verifica que los campos Marca, Modelo, Color, no esten en valor por default
        if self.comboMarca.get() == "Marca":
            return messagebox.showwarning("Genear Reporte","Error, selecciona una marca")
        elif self.comboModelo.get() == "Modelo":
            return messagebox.showwarning("Genear Reporte","Error, selecciona un modelo")
        elif self.comboColor.get() == "Color":
            return messagebox.showwarning("Genear Reporte","Error, selecciona un color")

        data_dict =  {
            "Camara" : f"{self.camara.get()}",
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
        #Verifica que marca no tenga valor por default 
        if self.comboMarca.get() == "Marca":
            return messagebox.showwarning("Genear Reporte","Error, selecciona una marca")

        self.valor = self.comboMarca.get()
        
        #Consulta la BD y trae de regreso los modelos de la marca seleccionada
        self.c2.execute("SELECT Modelo FROM MarcaModelo WHERE Marca = ? ORDER BY Modelo ASC", (self.valor,))
        
        #Verifica si la lista esta vacia, si lo esta, agrega los modelos de la consulta para la marca seleccionada
        if self.listaModelo == []:
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])
        #Si la lista no esta vacia, borra todo y posteriormente agrega los modelos de la consulta para la marca seleccionada
        else:
            del self.listaModelo [:]
            for modelo in  self.c2.fetchall():
                self.listaModelo.append(modelo[0])

        self.db.commit
        #Limpia el combobox de modelo
        self.comboModelo ["values"] = self.listaModelo
        self.comboModelo.set("Modelo")

    def visualizarVideo(self):
        #Limpia el valor para nueva selección de video
        self.cap = None

        #si el valor es no nada, se lanza el método release el cual bloquea el recurso en uso y, hasta que lo libera ningún otro subproceso puede acceder al mismo recurso
        if self.cap is not None:
            self.lblVideo.image = ""
            self.cap.release()
            self.cap = None

        #Selecciona el video según la cámara elegida en el combobox
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
        #Si el valor es no ninguno, lee
        if self.cap is not None:
            self.ret, self.frame = self.cap.read()
            if self.ret == True:
                self.frame = imutils.resize(self.frame, width=640)#Define el tamaño del frame
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)#Convierte el espacio de un color a otro y define el RGB para reproducir el video

                self.im = Img.fromarray(self.frame)#Crea una memoria de imagen a partir de un objeto que exporta la interfaz de matriz
                self.img = ImageTk.PhotoImage(image=self.im)#Se usa  donde Tkinter espere un objeto de imagen.

                self.lblVideo.configure(image=self.img)
                self.lblVideo.image = self.img
                self.lblVideo.after(10, self.visualizar)
            else:
                print("No se selecciono nada")
                self.lblVideo.image = ""
                self.cap.release()

    def selectRadioButton(self):
        if self.opcion.get() == 1:
            self.entryPlaca_var.set("A00-AAA / 000-AAA")
        else:
            self.entryPlaca_var.set("AAA-00-00")
        
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
