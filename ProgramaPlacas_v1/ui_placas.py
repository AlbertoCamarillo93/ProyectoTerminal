import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter.messagebox


#BLOQUE INTERFAZ
windowLogin = Tk() #Crea una instancia de tkinter
windowLogin.title ("Iniciar Sesión")
windowLogin.geometry ("350x150+500+250")

#CORREO
Label(windowLogin, text = "Correo:").pack()
boxEmail = Entry(windowLogin)
boxEmail.pack()

#PASSWORD
Label(windowLogin, text = "Contraseña:").pack()
boxPassword = Entry(windowLogin, show = "*")
boxPassword.pack()

#FUNCIÓN BOTÓN DE LOGEO
def login():
    # Connect to database
    db = sqlite3.connect('proyecto_placas.db')
    c = db.cursor()
    
    c.execute("SELECT * FROM Usuario WHERE correo=? AND password=?", (boxEmail.get(), boxPassword.get()))
    
    row = c.fetchall() 
    if row:
        if row[0][6] == 'admin':
            menuAdmin()
        elif row[0][6] == 'user':
            menuUser()
    else:
        tkinter.messagebox.showerror(title = "Login incorrecto", message = "Usuario o contraseña incorrecta")
  
    c.close()

Button (text = "Login", command = login).pack()


############### MENÚ ADMINISTRADOR ###############
def menuAdmin():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowMenuAdmin = Tk()
    windowMenuAdmin.geometry("350x200+500+250")
    windowMenuAdmin.title("Menu Administrador")
    Label(windowMenuAdmin, text = "Menu Administrador" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    
    #COLUMNA DE ETIQUETAS
    Label(windowMenuAdmin, text = "ID_Usuario" ).place(x=5, y=45)
    Label(windowMenuAdmin, text = "Nombre" ).place(x=5, y=75)
    Label(windowMenuAdmin, text = "Datos Contacto" ).place(x=5, y=105)

    #COLUMNA DE BOTONES
    Button(windowMenuAdmin, text = "Gestión de usuarios", command = gestionUsuarios).place(x=200, y=45, width=120, height=30)
    Button(windowMenuAdmin, text = "Reporte de placas", command = reportePlacas).place(x=200, y=90, width=120, height=30)
    Button(windowMenuAdmin, text = "Cerrar Sesión").place(x=240, y=160, width=100, height=30)


################ ADMINISTRADOR – GESTIÓN DE USUARIOS ###############
def gestionUsuarios():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuGestionUsuarios = Tk()
    windowSubmenuGestionUsuarios.geometry("350x200+500+250")
    windowSubmenuGestionUsuarios.title("Gestión Usuarios")
    Label(windowSubmenuGestionUsuarios, text = "Gestión Usuarios" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE BOTONES
    Button(windowSubmenuGestionUsuarios, text = "Crear Cuenta", command = crearCuenta).pack(padx= 5, pady = 5, ipadx = 15, ipady = 5)
    Button(windowSubmenuGestionUsuarios, text = "Modificar Cuenta",  command = modificarCuenta).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    Button(windowSubmenuGestionUsuarios, text = "Eliminar Cuenta",  command = eliminarCuenta).pack(padx= 5, pady = 5, ipadx = 10, ipady = 5)
    Button(windowSubmenuGestionUsuarios, text = "Regresar", command = menuAdmin).place(x=260, y=160, width=80, height=30)


################ ADMINISTRADOR - GESTIÓN DE USUARIOS – CREAR CUENTA ###############
def crearCuenta():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuGUCrearCuenta = Tk()
    windowSubmenuGUCrearCuenta.geometry("350x300+500+250")
    windowSubmenuGUCrearCuenta.title("Gestión Usuarios/Crear Cuenta")
    Label(windowSubmenuGUCrearCuenta, text = "Crear Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE LABES Y BOXES
    Label(windowSubmenuGUCrearCuenta, text = "Nombre:" ).place(x=5, y=45)
    boxName = Entry(windowSubmenuGUCrearCuenta).place(x=105, y=45, width=180, height=25)

    Label(windowSubmenuGUCrearCuenta, text = "Apellido Paterno:" ).place(x=5, y=75)
    boxLastname = Entry(windowSubmenuGUCrearCuenta).place(x=105, y=75,  width=180, height=25)

    Label(windowSubmenuGUCrearCuenta, text = "Contraseña" ).place(x=5, y=105)
    boxPassword = Entry(windowSubmenuGUCrearCuenta).place(x=105, y=105,  width=180, height=25)
    
    Label(windowSubmenuGUCrearCuenta, text = "Correo:").place(x=5, y=135)
    boxEmail = Entry(windowSubmenuGUCrearCuenta).place(x=105, y=135, width=180, height=25)

    #COLUMNA DE COMBOBOX
    Label(windowSubmenuGUCrearCuenta, text = "Asignar Cámara:").place(x=5, y=165)
    ttk.Combobox(windowSubmenuGUCrearCuenta, values=["Camara1",
                                                     "Camara2",]).place(x=105, y=165, width=100, height=25)

    Label(windowSubmenuGUCrearCuenta, text = "Tipo Usuario:").place(x=5, y=195)
    ttk.Combobox(windowSubmenuGUCrearCuenta, values=["Administrador",
                                                     "Usuario",]).place(x=105, y=195, width=100, height=25)
    
    #COLUMNA DE BOTONES
    Button(windowSubmenuGUCrearCuenta, text = "Crear").place(x=150, y=235, width=80, height=30)
    Button(windowSubmenuGUCrearCuenta, text = "Regresar", command = gestionUsuarios).place(x=260, y=260, width=80, height=30)  


################ ADMINISTRADOR – GESTIÓN DE USUARIOS – ELIMINAR CUENTA ############### 
def eliminarCuenta():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuGUEliminarCuenta = Tk()
    windowSubmenuGUEliminarCuenta.geometry("350x300+500+250")
    windowSubmenuGUEliminarCuenta.title("Gestión Usuarios/Eliminar Cuenta")
    Label(windowSubmenuGUEliminarCuenta, text = "Eliminar Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE COMBOBOX
    Label(windowSubmenuGUEliminarCuenta, text = "Eliminar Cuenta:").place(x=5, y=45)
    ttk.Combobox(windowSubmenuGUEliminarCuenta, values=["Usuario1",
                                                     "Usuario2",]).place(x=105, y=45, width=100, height=25)
    
    #COLUMNA DE BOTONES
    Button(windowSubmenuGUEliminarCuenta, text = "Confirmar").place(x=70, y=95, width=80, height=30)
    Button(windowSubmenuGUEliminarCuenta, text = "Regresar", command = gestionUsuarios).place(x=190, y=95, width=80, height=30)



################ ADMINISTRADOR – GESTIÓN DE USUARIO – MODIFICAR CUENTA ###############
def modificarCuenta():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuGUModificarCuenta = Tk()
    windowSubmenuGUModificarCuenta.geometry("350x300+500+250")
    windowSubmenuGUModificarCuenta.title("Gestión Usuarios/Modificar Cuenta")
    Label(windowSubmenuGUModificarCuenta, text = "Modificar Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE LABES, COMBOBOXES Y BOXES
    Label(windowSubmenuGUModificarCuenta, text = "Seleccionar Usuario:").place(x=5, y=45)
    ttk.Combobox(windowSubmenuGUModificarCuenta, values=["Camara1",
                                                     "Camara2",]).place(x=120, y=45, width=100, height=25)

    Label(windowSubmenuGUModificarCuenta, text = "Nombre:" ).place(x=5, y=75)
    boxName = Entry(windowSubmenuGUModificarCuenta).place(x=120, y=75, width=180, height=25)

    Label(windowSubmenuGUModificarCuenta, text = "Apellido Paterno:" ).place(x=5, y=105)
    boxLastname = Entry(windowSubmenuGUModificarCuenta).place(x=120, y=105,  width=180, height=25)

    Label(windowSubmenuGUModificarCuenta, text = "Contraseña" ).place(x=5, y=135)
    boxPassword = Entry(windowSubmenuGUModificarCuenta).place(x=120, y=135,  width=180, height=25)
    
    Label(windowSubmenuGUModificarCuenta, text = "Correo:").place(x=5, y=165)
    boxEmail = Entry(windowSubmenuGUModificarCuenta).place(x=120, y=165, width=180, height=25)

    Label(windowSubmenuGUModificarCuenta, text = "Tipo Usuario:").place(x=5, y=195)
    ttk.Combobox(windowSubmenuGUModificarCuenta, values=["Administrador",
                                                     "Usuario",]).place(x=120, y=195, width=100, height=25)
    
    #COLUMNA DE BOTONES
    Button(windowSubmenuGUModificarCuenta, text = "Modificar").place(x=140, y=235, width=80, height=30)
    Button(windowSubmenuGUModificarCuenta, text = "Regresar", command = gestionUsuarios).place(x=250, y=250, width=80, height=30)


################ ADMINISTRADOR – REPORTE DE PLACAS ###############
def reportePlacas():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuReportePlacas = Tk()
    windowSubmenuReportePlacas.geometry("350x200+500+250")
    windowSubmenuReportePlacas.title("Reporte de Placas")
    Label(windowSubmenuReportePlacas, text = "Reporte de Placas" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE BOTONES
    Button(windowSubmenuReportePlacas, text = "Obtener Reporte de Alertas", command = obtenerReporte).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    Button(windowSubmenuReportePlacas, text = "Generar Reporte de Busqueda",  command = generarReporte).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    Button(windowSubmenuReportePlacas, text = "Regresar", command = menuAdmin).place(x=260, y=160, width=80, height=30)


################ ADMINISTRADOR – REPORTE DE PLACAS – GENERAR REPORTE ###############
def generarReporte():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuRPGenerarReporte = Tk()
    windowSubmenuRPGenerarReporte.geometry("350x300+500+250")
    windowSubmenuRPGenerarReporte.title("Reporte de Placas/Generar Reporte")
    Label(windowSubmenuRPGenerarReporte, text = "Generar Reporte" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE LABES, BOXES
    Label(windowSubmenuRPGenerarReporte, text = "Placa:" ).place(x=5, y=45)
    boxPlate = Entry(windowSubmenuRPGenerarReporte).place(x=105, y=45, width=180, height=25)

    Label(windowSubmenuRPGenerarReporte, text = "Modelo:" ).place(x=5, y=75)
    boxModel = Entry(windowSubmenuRPGenerarReporte).place(x=105, y=75, width=180, height=25)

    Label(windowSubmenuRPGenerarReporte, text = "Color:" ).place(x=5, y=105)
    boxColor = Entry(windowSubmenuRPGenerarReporte).place(x=105, y=105,  width=180, height=25)

    #COLUMNA DE BOTONES
    Button(windowSubmenuRPGenerarReporte, text = "Aceptar").place(x=130, y=140,  width=80, height=25)
    Button(windowSubmenuRPGenerarReporte, text = "Regresar", command = reportePlacas).place(x=240, y=200, width=80, height=30)


################ ADMINISTRADOR – REPORTE DE PLACAS – OBTENER REPORTE ###############
def obtenerReporte():
    windowLogin.withdraw() #Oculta la ventana sin destruirla internamente
    windowSubmenuRPGenerarReporte = Tk()
    windowSubmenuRPGenerarReporte.geometry("350x400+500+250")
    windowSubmenuRPGenerarReporte.title("Reporte de Placas/Obtener Reporte")
    Label(windowSubmenuRPGenerarReporte, text = "Obtener Reporte" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

    #COLUMNA DE LABES, BOXES
    Label(windowSubmenuRPGenerarReporte, text = "Ingresa la placa para obtener el reporte:" ).place(x=5, y=45)
    boxName = Entry(windowSubmenuRPGenerarReporte).place(x=5, y=75, width=150, height=25)
    Button(windowSubmenuRPGenerarReporte, text = "Aceptar").place(x=170, y=75, width=80, height=30)

    Label(windowSubmenuRPGenerarReporte, text = "El reporte generado es:" ).place(x=5, y=110)
    boxLastname = Entry(windowSubmenuRPGenerarReporte).place(x=5, y=140,  width=330, height=185)

    #COLUMNA DE BOTONES
    Button(windowSubmenuRPGenerarReporte, text = "Guardar").place(x=135, y=335, width=80, height=30)#AQUI PORNER UN MENSAJE DE SE GUARDO CORRECTAMENTE
    Button(windowSubmenuRPGenerarReporte, text = "Regresar", command = reportePlacas).place(x=250, y=360, width=80, height=30)


################ MENÚ USUARIO ###############
def menuUser():
    windowLogin.withdraw()
    windowMenuUser = Tk()
    windowMenuUser.geometry("400x300+500+250")
    windowMenuUser.title("Menu Usuario")
    Label(windowMenuUser, text = "Menu Usuario" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
   
    #COLUMNA DE ETIQUETAS
    Label(windowMenuUser, text = "ID_Usuario" ).place(x=5, y=45)
    Label(windowMenuUser, text = "Nombre" ).place(x=5, y=75)
    Label(windowMenuUser, text = "Cámara" ).place(x=5, y=105)
    Label(windowMenuUser, text = "Datos Contacto" ).place(x=5, y=135)

    #COLUMNA DE BOTONES
    Button(windowMenuUser, text = "Obtener Reporte de Alertas", command = obtenerReporte).place(x=200, y=45, width=180, height=30)#CREAR CONDICION EN OBTENER REPORTE PARA QUE CUANDO VENGA DESDE EL MENU DE USUARIO NO ME MEZCLE CON EL MENU DE ADMINISTRADOR
    Button(windowMenuUser, text = "Monitorear Cámara", command = monitorearCamara).place(x=200, y=90, width=180, height=30)
    Button(windowMenuUser, text = "Cerrar Sesión").place(x=270, y=260, width=100, height=30)


################ MENÚ USUARIO – MONITOREAR CÁMARA ###############
def monitorearCamara():
    windowLogin.withdraw()
    global windowSubmenuMonitoreaCamara
    windowSubmenuMonitoreaCamara = Tk()
    windowSubmenuMonitoreaCamara.geometry("400x300+500+250")
    windowSubmenuMonitoreaCamara.title("Menu Usuario/Monitorear Cámara")
    Label(windowSubmenuMonitoreaCamara, text = "Monitorear Cámara" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    
    #COLUMNA DE COMBOBOX    
    Label(windowSubmenuMonitoreaCamara, text = "Seleccionar Cámara:").place(x=5, y=45)
    ttk.Combobox(windowSubmenuMonitoreaCamara, values=["Camara1",
                                                     "Camara2",]).place(x=120, y=45, width=100, height=25)

    #COLUMNA DE ETIQUETAS
    Label(windowSubmenuMonitoreaCamara, text = "Datos de la placa detectada" ).place(x=5, y=75)
    Label(windowSubmenuMonitoreaCamara, text = "Placa" ).place(x=5, y=105)
    Label(windowSubmenuMonitoreaCamara, text = "Modelo" ).place(x=5, y=135)
    Label(windowSubmenuMonitoreaCamara, text = "Color" ).place(x=5, y=165)

    #COLUMNA DE BOTONES
    Button(windowSubmenuMonitoreaCamara, text = "Generar Reporte", command = generarReporte).place(x=10, y=260, width=120, height=30)#MISMO QUE OBTENER REPORTE DE MENU USUARIO
    Button(windowSubmenuMonitoreaCamara, text = "Visualizar Alerta", command = visualizarAlerta).place(x=140, y=260, width=120, height=30)
    Button(windowSubmenuMonitoreaCamara, text = "Regresar", command = menuUser).place(x=270, y=260, width=100, height=30)

################ MENÚ USUARIO – MONITOREAR CÁMARA – VISUALIZAR ALERTA ###############
def visualizarAlerta():
    windowSubmenuMonitoreaCamara.withdraw()
    windowSubmenuVisualiza = Tk()
    windowSubmenuVisualiza.geometry("500x350+500+250")
    windowSubmenuVisualiza.title("Monitorear Cámara/Visualizar Alerta")
    Label(windowSubmenuVisualiza, text = "Visualizar Alerta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    
    #COLUMNA DE ETIQUETAS
    Label(windowSubmenuVisualiza, text = "Placa" ).place(x=5, y=45)
    Label(windowSubmenuVisualiza, text = "Modelo" ).place(x=5, y=75)
    Label(windowSubmenuVisualiza, text = "Color" ).place(x=5, y=105)

    #COLUMNA DE BOTONES
    Button(windowSubmenuVisualiza, text = "Regresar", command = monitorearCamara).place(x=200, y=300, width=100, height=30)
    #windowSubmenuVisualiza.
            


windowLogin.mainloop() #EJECUTA EN VENTANA PRINCIPAL LA VENTANA
