import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GestionarUsuarioCrear:
    
    ################ ADMINISTRADOR - GESTIÓN DE USUARIOS – CREAR CUENTA ###############
    def __init__(self, args):
        #Conexión bd
        self.db = sqlite3.connect('proyecto_placas_pruebas.db')
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
        
        self.buttonRegresar = Button(self.windowSubmenuGUCrearCuenta, text = "Regresar")#, command = lambda : GestionarUsuario(self.windowSubmenuGUCrearCuenta.withdraw()))
        self.buttonRegresar.place(x=200, y=240, width=80, height=30)

        self.windowSubmenuGUCrearCuenta.mainloop()
               
    #CREAR MENSAJES DE ERROR Y EXITO SEGUN SEA EL CASO
    def crearUsuario(self):
        
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboAsignarCamara.get() == "Elige una opción":
            return messagebox.showwarning("Crear Usuario","Error, ningun campo puede quedar vacio")
        elif len(self.boxPassword.get()) < 4:
            return messagebox.showwarning("Crear Usuario","Error, la contraseña debe tener al menos 4 digitos")
        elif self.boxEmail.get().find('@') == -1:
            return messagebox.showwarning("Crear Usuario","Error, no es un correo valido")
        elif self.boxEmail.get().find('.com') == -1:
            return messagebox.showwarning("Crear Usuario","Error, no es un correo valido")
        

        
        ###
        #self.c3 = self.db.cursor()
        #self.c3.execute("SELECT DISTINCT correo FROM Usuario WHERE correo = ?", (self.boxEmail.get(),)) 
       #print("self.boxEmail.get():", self.boxEmail.get())
        
        self.c4 = self.db.cursor()
        self.c4.execute("SELECT correo FROM Usuario") 
        
        self.listaCorreoSeleccionado = []
        self.listaCorreoSeleccionado.append(self.boxEmail.get())
        #for row in self.c3.fetchall():
        #    self.listaCorreoSeleccionado.append(row[0])
        #print("1self.listaCorreoSeleccionado:", self.listaCorreoSeleccionado)

        self.listaCorreos = []
        for row in self.c4.fetchall():
            self.listaCorreos.append(row[0])
        #print("1self.listaCorreos:", self.listaCorreos)

        
        #if self.listaCorreos != []:
        #   del self.listaCorreos[-1]
        #print("2self.listaCorreos:", self.listaCorreos)

        n=0
        for i in self.listaCorreos:
            #del self.listaCorreos[-1]
            #print("i:", i)
            #print("self.listaCorreoSeleccionado[0]: ", self.listaCorreoSeleccionado[0])
            #print(f"self.listaCorreos[{n}]: ", self.listaCorreos[n])
            n+=1
            if  self.listaCorreoSeleccionado[0] not in self.listaCorreos   :
                #del self.listaCorreos[:]
                self.listaCorreos.append(self.listaCorreoSeleccionado[0])
                break  
            elif self.listaCorreos[n] == self.listaCorreoSeleccionado[0]:
                #elimina = self.listaCorreoSeleccionado[0]
                #del self.listaCorreos[:]
                #print("elif --> self.listaCorreos: ", self.listaCorreos)
                return messagebox.showwarning("Crear Usuario","Error, el correo ya existe")
            #print("3self.listaCorreos: ", self.listaCorreos)
                               
        #print("4self.listaCorreos:", self.listaCorreos)

        self.c = self.db.cursor()

        self.datos = self.comboAsignarCamara.get(), self.boxName.get().capitalize(),self.boxLastname.get().capitalize(),self.boxPassword.get(),self.boxEmail.get(),self.comboTipoUsuario.get()
        self.c.execute("INSERT INTO Usuario VALUES(NULL,?,?,?,?,?,?)", (self.datos))  
        ### 
        self.db.commit()

        self.boxName.delete(0, 'end')
        self.boxLastname.delete(0, 'end')
        self.boxPassword.delete(0, 'end')
        self.boxEmail.delete(0, 'end')
        self.comboTipoUsuario.set("Elige una opción")
        self.comboAsignarCamara.set("Elige una opción")

        messagebox.showinfo("Crear Usuario","Registro insertado con éxito")

args = ""
GestionarUsuarioCrear(args)