from tkinter import Button, Entry, IntVar, Label, StringVar, Tk, Toplevel
from typing import Text
import config
#from typing_extensions import IntVar


class Uno:

    def __init__(self, args):

        self.primarywindow = Tk()
        self.primarywindow.title ("Iniciar Sesión")
        self.primarywindow.geometry ("350x150+500+250")

        #numero1
        self.numOne = Entry(self.primarywindow)
        self.numOne.pack()
        
        #numero2
        self.numTwo = Entry(self.primarywindow)
        self.numTwo.pack()

        Button(self.primarywindow, text ="sumar", command=self.suma).pack()
        Button(self.primarywindow, text ="next", command=self.nextWindow).pack()

        self.primarywindow.mainloop()

    def suma(self):
        a = int(self.numOne.get())
        b = int(self.numTwo.get())
        self.suma_ab = a + b
        print(self.suma_ab)
        config.suma_ab = self.suma_ab

    def nextWindow(self):
        Dos(self)
        self.primarywindow.withdraw() 
        
    def sumaRetorna(self):
        #return print("ok")
        
        return print("A",config.suma_ab)
    

class Dos:
    def __init__(self, args):

        self.secundarywindow = Toplevel()
        self.secundarywindow.title ("Iniciar Sesión")
        self.secundarywindow.geometry ("350x150+500+250")

        self.numSum_var = IntVar()
        self.numSum = Entry(self.secundarywindow, textvariable=self.numSum_var)
        self.numSum.pack()
        
        Button(self.secundarywindow, text ="recupera", command=self.recupera).pack()


    def recupera(self):
        
        self.numSum_var.set(config.suma_ab)
        print("B",config.suma_ab)
        
        return Uno.sumaRetorna(self)
        #self.__class__.sumaRetorna(self)


