import config
from windows import *
from tkinter import *

args = ''

window = Login(args)

config.apellido = Login.prueba(args)
config.camara = Login.prueba(args)
config.contacto_usuario = Login.prueba(args)
config.id_usuario = Login.prueba(args)
config.nombre = Login.prueba(args)