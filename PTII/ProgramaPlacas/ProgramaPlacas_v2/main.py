import config
from windows import *
from tkinter import *

args = ''

window = Login(args)

config.apellido = Login.obtieneVariablesGlobales(args)
config.camara = Login.obtieneVariablesGlobales(args)
config.contacto_usuario = Login.obtieneVariablesGlobales(args)
config.id_usuario = Login.obtieneVariablesGlobales(args)
config.nombre = Login.obtieneVariablesGlobales(args)