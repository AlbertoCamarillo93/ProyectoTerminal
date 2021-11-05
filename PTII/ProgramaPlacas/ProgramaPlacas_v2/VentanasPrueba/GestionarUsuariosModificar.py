from tkinter import Entry, Frame, IntVar, StringVar, Toplevel, messagebox, Label, Button, Tk
from tkinter import ttk
import sqlite3

from windows import GestionarUsuario

class GestionarUsuarioModificar:  
    ################ ADMINISTRADOR – GESTIÓN DE USUARIO – MODIFICAR CUENTA ###############
    def __init__(self, args):

        self.db = sqlite3.connect('proyecto_placas.db')  
        self.c = self.db.cursor()
        self.c.execute("SELECT correo FROM Usuario ORDER BY correo ASC ")   

        self.result = []

        for row in self.c.fetchall():
            self.result.append(row[0])

        self.windowSubmenuGUModificarCuenta = Toplevel()
        self.windowSubmenuGUModificarCuenta.geometry("350x350+500+250")
        self.windowSubmenuGUModificarCuenta.title("Gestión Usuarios/Modificar Cuenta")
        Label(self.windowSubmenuGUModificarCuenta, text = "Modificar Cuenta" ).pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)

        #COLUMNA DE LABES, COMBOBOXES Y BOXES
        Label(self.windowSubmenuGUModificarCuenta, text = "Seleccionar Usuario:").place(x=5, y=45)
        self.user = ttk.Combobox(self.windowSubmenuGUModificarCuenta, values = self.result)
        self.user.place(x=120, y=45, width=100, height=25)

        self.buttonBuscar = Button(self.windowSubmenuGUModificarCuenta, text = "Buscar", command = self.leer)
        self.buttonBuscar.place(x=230, y=45, width=80, height=25)

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

        Label(self.windowSubmenuGUModificarCuenta, text = "Tipo Usuario:").place(x=5, y=195)
        self.comboTipoUsuario = ttk.Combobox(self.windowSubmenuGUModificarCuenta, values=["admin", "user",])
        self.comboTipoUsuario.place(x=120, y=195, width=100, height=25)

        Label(self.windowSubmenuGUModificarCuenta, text = "Seleccionar Camara:").place(x=5, y=225)
        self.comboCamara = ttk.Combobox(self.windowSubmenuGUModificarCuenta, values=["1", "2",])
        self.comboCamara.place(x=120, y=225, width=100, height=25)

        
        #COLUMNA DE BOTONES
        self.buttonModificar = Button(self.windowSubmenuGUModificarCuenta, text = "Modificar", command = self.modificarUsuario)
        self.buttonModificar.place(x=140, y=265, width=80, height=30)

        #self.buttonRegresar  = Button(self.windowSubmenuGUModificarCuenta, text = "Regresar", command = lambda : GestionarUsuario(self.windowSubmenuGUModificarCuenta.withdraw()))
        #self.buttonRegresar.place(x=250, y=250, width=80, height=30)

        self.idUsuario_var = IntVar()
        
        self.windowSubmenuGUModificarCuenta.mainloop()

    def modificarUsuario(self):
        
        #self.db = sqlite3.connect('proyecto_placas.db')
        #self.c = self.db.cursor()

        self.c.execute("SELECT * FROM Usuario WHERE correo = ?", (self.valor,))
        elUsuario=self.c.fetchall()
        
        for usuario in elUsuario:
            self.idUsuario_var.set(usuario[0])
        print(self.idUsuario_var.get())
        
        self.datos = self.comboCamara.get(), self.boxName.get(), self.boxLastname.get(), self.boxPassword.get(), self.boxEmail.get(), self.comboTipoUsuario.get(), self.idUsuario_var.get()
        self.c.execute("UPDATE Usuario SET  id_camara = ?, nombre = ?, apellido_p = ?, password = ?, correo = ?, tipoUsuario = ? WHERE idUsuario = ?", (self.datos))  
        self.db.commit()
    
        messagebox.showinfo("BBDD","Registro actualizado con éxito")

    def leer(self):
        
        #self.db = sqlite3.connect('proyecto_placas.db')
        #self.c = self.db.cursor()

        self.valor = self.user.get()

        self.c.execute("SELECT * FROM Usuario WHERE correo = ?", (self.valor,))
        elUsuario=self.c.fetchall()
        
        for usuario in elUsuario:
            
            self.boxName_var.set(usuario[2])
            self.boxLastname_var.set(usuario[3])
            self.boxPassword_var.set(usuario[4])
            self.boxEmail_var.set(usuario[5])
            self.comboTipoUsuario.set(usuario[6])
            self.comboCamara.set(usuario[1])
            
        print( self.boxName_var.get(), self.boxLastname_var.get(), 
        self.boxPassword_var.get(),self.boxEmail_var.get(),
        self.comboTipoUsuario.get(),self.comboCamara.get())

        self.db.commit()

args = ""
GestionarUsuarioModificar(args)