from tkinter import Entry, IntVar, Radiobutton,  StringVar, Label, Button, Tk, Toplevel, messagebox, ttk
from PIL import Image



def main():
    windowSubmenuMonitoreaCamara = Tk()
    ancho_ventana = 450
    alto_ventana = 500
    x_ventana =  windowSubmenuMonitoreaCamara.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana =   windowSubmenuMonitoreaCamara.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    windowSubmenuMonitoreaCamara.geometry(posicion)
    windowSubmenuMonitoreaCamara.title("Menu Usuario/Monitorear Cámara")
    labeltitulo = Label(windowSubmenuMonitoreaCamara, text = "Monitorear Cámara" )
    labeltitulo.pack(padx= 5, pady = 5, ipadx = 5, ipady = 5)
    labeltitulo.config(font=16)

    buttonGenerar = Button(windowSubmenuMonitoreaCamara, text = "Generar Reporte de Alerta", command = generarReporteAlerta())
    buttonGenerar.place(x=10, y=38, width=160, height=30 )
    windowSubmenuMonitoreaCamara.mainloop()


def generarReporteAlerta():
    archivo_png = "ocrDetect1.png"
    im = Image.open(f"D:\Aplicaciones\Yolo_v4\yolov4-custom-functions\detections\\archivosTxtOCR\\{archivo_png}")
    im.show()

    return messagebox.showinfo("Alerta de Visualización", im.show())

main()