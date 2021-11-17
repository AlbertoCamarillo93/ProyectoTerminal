import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GestionarUsuarioModificar:  
    ################ ADMINISTRADOR – GESTIÓN DE USUARIO – MODIFICAR CUENTA ###############
    def __init__(self, args):

        self.db = sqlite3.connect('proyecto_placas_pruebas.db')  
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

        self.windowSubmenuGUModificarCuenta = Tk()
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

        self.buttonRegresar  = Button(self.windowSubmenuGUModificarCuenta, text = "Regresar")#, command = lambda : GestionarUsuario(self.windowSubmenuGUModificarCuenta.withdraw()))
        self.buttonRegresar.place(x=220, y=265, width=80, height=30)

        self.idUsuario_var = IntVar()

        self.windowSubmenuGUModificarCuenta.mainloop()

    def modificarUsuario(self):
        if self.boxName.get() == "" or self.boxLastname.get() == "" or self.boxPassword.get() == "" or self.boxEmail.get() == "" or self.comboTipoUsuario.get() == "Elige una opción" or self.comboCamara.get() == "Elige una opción":
            return messagebox.showwarning("Modificar Usuario","Error, ningun campo puede quedar vacio")
        elif len(self.boxPassword.get()) < 4:
            return messagebox.showwarning("Modificar Usuario","Error, la contraseña debe tener al menos 4 digitos")
        elif self.boxEmail.get().find('@') == -1:
            return messagebox.showwarning("Modificar Usuario","Error, no es un correo valido")
        elif self.boxEmail.get().find('.com') == -1:
            return messagebox.showwarning("Modificar Usuario","Error, no es un correo valido")
        
        self.datos = self.comboCamara.get(), self.boxName.get(), self.boxLastname.get(), self.boxPassword.get(), self.boxEmail.get(), self.comboTipoUsuario.get(), self.idUsuario_var.get()
        self.c.execute("UPDATE Usuario SET  id_camara = ?, nombre = ?, apellido_p = ?, password = ?, correo = ?, tipoUsuario = ? WHERE idUsuario = ?", (self.datos))        

        self.comboUser.set("Elige una opción")
        self.boxName.delete(0, 'end')
        self.boxLastname.delete(0, 'end')
        self.boxPassword.delete(0, 'end')
        self.boxEmail.delete(0, 'end')
        self.comboTipoUsuario.set("Elige una opción")
        self.comboCamara.set("Elige una opción")

        ##CAMBIO AQUI#####
        n = 0
        for row in self.result:
            if self.comboUser.get() == row:
                del self.result[n]
            n+= 1
        self.comboUser ["values"]= self.result
        self.comboUser.set("Elige una opción")

        ##CAMBIO AQUI#####

        self.db.commit()##CAMBIO AQUI#####
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

        self.comboUser.set("Elige una opción") ###CAMBIO AQUI
        self.db.commit()

args=''
GestionarUsuarioModificar(args)