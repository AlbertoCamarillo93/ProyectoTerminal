import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GestionarUsuarioElimina():

    def __init__(self, args):

        self.db = sqlite3.connect('proyecto_placas_pruebas.db')  
        self.c = self.db.cursor()
        self.c.execute("SELECT correo FROM Usuario ORDER BY correo ASC ")   

        self.result = []

        for row in self.c.fetchall():
            self.result.append(row[0])

        self.windowSubmenuGUEliminarCuenta = Tk()
        self.windowSubmenuGUEliminarCuenta.geometry("350x200+500+250")
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
        
        self.buttonRegresar = Button(self.windowSubmenuGUEliminarCuenta, text = "Regresar")#, command = lambda : GestionarUsuario(self.windowSubmenuGUEliminarCuenta.withdraw()))
        self.buttonRegresar.place(x=190, y=95, width=80, height=30)

        self.windowSubmenuGUEliminarCuenta.mainloop()

    def eliminarCuenta(self):
        if self.comboEliminar.get() == "Elige una opción":
                return messagebox.showwarning("Eliminar Usuario","Error, selecciona un usuario")

        self.c1 = self.db.cursor()
        self.valor = self.comboEliminar.get()
        self.c1.execute("DELETE FROM Usuario WHERE correo = ?", (self.valor,))                 
        
        n = 0
        for row in self.result:
            if self.comboEliminar.get() == row:
                del self.result[n]
            n+= 1
        self.comboEliminar ["values"]= self.result
        self.comboEliminar.set("Elige una opción")

        self.db.commit()
        
        messagebox.showinfo("Eliminar Usuario","Registro borrado con éxito") 
        

args = ""
GestionarUsuarioElimina(args)