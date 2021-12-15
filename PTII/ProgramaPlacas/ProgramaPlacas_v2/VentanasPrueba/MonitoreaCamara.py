import glob
import json
import os
import shutil
import boto3
import config
import sqlite3
import pytesseract
import cv2
import re
from tkinter import Entry, IntVar, Radiobutton,  StringVar, Label, Button, Tk, Toplevel, messagebox, ttk



class MonitoreaCamara:


    ################ MENÚ USUARIO – MONITOREAR CÁMARA ###############
    def __init__(self, args):

        #Conecta a la BD
        self.db = sqlite3.connect('D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/ProyectoTerminal/ProgramaPlacas_v2/proyecto_placas.db')
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
        ancho_ventana = 450
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
        Label(self.windowSubmenuMonitoreaCamara, text = "Datos de la placa detectada" ).place(x=150, y=70)
        
        #RADIOBUTTON
        self.opcion = IntVar()
        self.buttonCDMX = Radiobutton(self.windowSubmenuMonitoreaCamara, text="Ciudad de México", variable= self.opcion, value=1, command= self.selectRadioButton)
        self.buttonCDMX.place(x=150, y=90)
        self.buttonEdoMex = Radiobutton(self.windowSubmenuMonitoreaCamara, text="Estado de México", variable= self.opcion, value=2, command= self.selectRadioButton)
        self.buttonEdoMex.place(x=150, y=110)

        #Placa
        Label(self.windowSubmenuMonitoreaCamara, text = "Placa" ).place(x=150, y=130)
        self.entryPlaca_var = StringVar()
        self.entryPlaca = Entry(self.windowSubmenuMonitoreaCamara, textvariable = self.entryPlaca_var)
        self.entryPlaca.place(x=150, y=150, width=160, height=25)

        #Marca
        Label(self.windowSubmenuMonitoreaCamara, text = "Marca" ).place(x=150, y=180)
        self.comboMarca = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values = self.resultMarca)
        self.comboMarca.set("Marca")
        self.comboMarca.place(x=150, y=200, width=160, height=25)
        self.buttonBuscarModelo = Button(self.windowSubmenuMonitoreaCamara, text = "Buscar Modelo", command = self.obtenerModelo)
        self.buttonBuscarModelo.place(x=150, y=230, width=160, height=30)

        #Modelo
        Label(self.windowSubmenuMonitoreaCamara, text = "Modelo" ).place(x=150, y=270)
        self.comboModelo = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaModelo) 
        self.comboModelo.set("Modelo")
        self.comboModelo.place(x=150, y=290, width=160, height=25)

        #Color
        Label(self.windowSubmenuMonitoreaCamara, text = "Color" ).place(x=150, y=320)
        self.comboColor = ttk.Combobox(self.windowSubmenuMonitoreaCamara,  state = "readonly", values =  self.listaColores) 
        self.comboColor.set("Color")
        self.comboColor.place(x=150, y=340, width=160, height=25)

        #Video
        self.lblVideo = Label(self.windowSubmenuMonitoreaCamara, text = "" )
        self.lblVideo.place(x=0, y=0)

        #COLUMNA DE BOTONES
        self.buttonGenerar = Button(self.windowSubmenuMonitoreaCamara, text = "Generar Reporte de Alerta", command = self.generarReporteAlerta)
        self.buttonGenerar.place(x=150, y=380, width=160, height=30 )
        #self.buttonVisualizar = Button(self.windowSubmenuMonitoreaCamara, text = "Visualizar Alerta", command = lambda : VisualizarReporteAlerta.visualizarAlerta(self, self.windowSubmenuMonitoreaCamara.withdraw()))
        #self.buttonVisualizar.place(x=10, y=260, width=120, height=30)
        self.buttonLimpiar = Button(self.windowSubmenuMonitoreaCamara, text = "Limpiar", command = self.LimpiarWidgets)#, command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        self.buttonLimpiar.place(x=150, y=420, width=160, height=30)
        self.buttonRegresar = Button(self.windowSubmenuMonitoreaCamara, text = "Regresar")#, command = lambda : User(self.windowSubmenuMonitoreaCamara.withdraw()))
        self.buttonRegresar.place(x=150, y=460, width=160, height=30)

        self.windowSubmenuMonitoreaCamara.mainloop()

    def LimpiarWidgets(self):
        self.opcion.set(0)
        self.entryPlaca.delete(0, 'end')
        self.comboMarca.set("Marca")
        self.comboModelo.set("Modelo")
        self.comboColor.set("Color")

    def selectRadioButton(self):
        if self.opcion.get() == 1:
            self.entryPlaca_var.set("A00-AAA / 000-AAA")
        else:
            self.entryPlaca_var.set("AAA-00-00")

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

        fname = 'D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/ProyectoTerminal/ProgramaPlacas_v2/ReporteAlerta.json'
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
        cv2.destroyAllWindows()
        self.upload_to_aws()

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
               
        #Selecciona el video según la cámara elegida en el combobox
        self.video_path = ''
        if  self.camara.get() == "1":
            self.video_path_var = "00032"
            self.video_path = os.system("D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/batch_00010.bat")
        elif self.camara.get() == "2":
            self.video_path_var = "00032"
            self.video_path = os.system("D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/batch_00017.bat")
        elif self.camara.get() == "3":
            self.video_path_var = "00032"
            self.video_path = os.system("D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/batch_00027.bat")
        elif self.camara.get() == "4":
            self.video_path_var = "00032"
            self.video_path = os.system("D:/Aplicaciones/Yolo_v4/yolov4-custom-functions/batch_00031.bat")
        else:
            messagebox.showwarning("Visualizar video","No se seleccionó cámara")

        self.camara.set(config.camara)
        self.moverImagenes()
        self.OCR()
        self.txt_ocr_compara()
        self.visualizaAlerta()
                   
    def moverImagenes(self):
        n = 1
        rootDir = f'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\crop\\{self.video_path_var}'
        files = os.listdir(rootDir)
        for dirName, subdirList, files in os.walk(rootDir, topdown=False):
            #print('Directorio encontrado: %s' % dirName)
            for file in files:
                destination = f'D:\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR\\PlacaVehicular_{n}.png'
                new_path = shutil.move(f"{dirName}/{file}", destination)
                n += 1 
                #print(new_path)
        
    def OCR(self):
        imagenes_path = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR'
        imagenes = os.listdir(imagenes_path)

        n = 1
        for imagen in imagenes:

            imagen_path = imagenes_path + '/' + imagen

            # point to license plate image (works well with custom crop function)
            gray = cv2.imread(imagen_path, 0)
            if gray is None: continue

            gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            gray = cv2.medianBlur(gray, 3)
            # perform otsu thresh (using binary inverse since opencv contours work better with white text)
            ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            #cv2.imshow("Otsu", thresh)
            #cv2.waitKey(0)
            rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

            # apply dilation 
            dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
            # find contours
            try:
                contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            except:
                ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

            # create copy of image
            im2 = gray.copy()

            plate_num = ""

            # loop through contours and find letters in license plate
            for cnt in sorted_contours:
                x,y,w,h = cv2.boundingRect(cnt)
                height, width = im2.shape
                
                # if height of box is not a quarter of total height then skip
                if height / float(h) > 6: continue
                ratio = h / float(w)
                # if height to width ratio is less than 1.5 skip
                if ratio < 1.5: continue
                area = h * w
                # if width is not more than 25 pixels skip
                if width / float(w) > 35: continue
                # if area is less than 100 pixels skip
                if area < 100: continue
                # draw the rectangle
                rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),2)
                roi = thresh[y-20:y+h+20, x-10:x+w+10]
                roi = cv2.bitwise_not(roi)
                roi = cv2.medianBlur(roi, 5)
                text = pytesseract.image_to_string(roi, config='-c tessedit_char_whitelist=-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 13 --oem 3')#8 --oem 3')
                #print(text)
                plate_num += text
                plate_num = re.sub(r'[^\da-zA-Z]+', '', plate_num) #Permite solo caracteres alfanumericos, los demas los elimina. 
            
            if len(plate_num) < 5:
                continue
            else:     
                file = open(f"D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR\\ocrDetect{n}.txt", "wb")
                file.write(plate_num.encode())
                destination = f'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR\\ocrDetect{n}.png'
                new_path = shutil.move(f"{imagenes_path}/{imagen}", destination)
                print("placa:", plate_num)
                n += 1

        folder = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #Elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
       
    def txt_ocr_compara(self):
        #Bloque que lee el archivo JSON y lo almacena en una lista
        file_json = open("D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\ProyectoTerminal\\ProgramaPlacas_v2\\PlacasReporteBusqueda.json", "r")
        content_json =  file_json.read()
        plates = json.loads(content_json)
        lista_Placa_json = []
        for plate in plates ["Automoviles"]:
            placa_auto = plate["Placa"]
            placa_auto = re.sub(r'[^\da-zA-Z]+', '', placa_auto)
            lista_Placa_json.append(placa_auto)

        #Bloque que lee el archivo txt y guarda cada linea del texto como un elemento dentro de una lista
        txt_path = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR'
        txt_files = os.listdir(txt_path)
        #print("txt_files: ", txt_files)

        lista_Placa_txt = []
        
        config.lista_archivos_png = []
        for txt_file in txt_files:
            if txt_file.endswith(".txt"):
                #print(txt_file)
                with open(f"{txt_path}/{txt_file}") as file_txt:
                    rows = file_txt.readlines()
                    for row in rows:
                        while '' in lista_Placa_txt:
                            lista_Placa_txt.remove('')
                        content_txt = file_txt.read()
                        lista_Placa_txt.append(row.strip('\n'))
                        while '' in lista_Placa_txt:
                            lista_Placa_txt.remove('')
            elif txt_file.endswith(".png"):
                config.lista_archivos_png.append(txt_file)
        
        print("Lista de placas en txt: ", lista_Placa_txt)
        print("Lista de placas en png: ", config.lista_archivos_png)

        #Bloque para comparar las dos cadenas JSON-TXT
        i = 0
        config.listaCompara_OcrTxt = []
        for atxt in lista_Placa_txt:
            for aJson in lista_Placa_json:
                if atxt in aJson:
                    config.listaCompara_OcrTxt.append(aJson)
                    self.archivo_png = config.lista_archivos_png[i]
                    print("lista_archivos_png.index(i)", self.archivo_png)
            i += 1
        print("listaCompara_OcrTxt: ",config.listaCompara_OcrTxt)

        #Regresa todos los valores de la placa detectada, recorriendo de nuevo el Json
        for x in config.listaCompara_OcrTxt:
            for placa in plates ["Automoviles"]:
                placa_auto1 = placa["Placa"]
                placa_auto1 = re.sub(r'[^\da-zA-Z]+', '', placa_auto1)
                if placa_auto1 == x:
                    self.placa_var  = placa["Placa"]
                    self.marca_var  = placa["Marca"]
                    self.modelo_var = placa["Modelo"]
                    self.color_var  = placa["Color"] 

    def visualizaAlerta(self):
        for comparacion in config.listaCompara_OcrTxt:
            if len(comparacion) == 7:
                self.opcion.set(2)
                self.entryPlaca.insert(0, self.placa_var)
                self.comboMarca.set(self.marca_var)
                self.comboModelo.set(self.modelo_var)
                self.comboColor.set(self.color_var)
                
                self.imagen_png = f"D:\Aplicaciones\Yolo_v4\yolov4-custom-functions\detections\\archivosTxtOCR\\{self.archivo_png}"
                cv_img = cv2.imread(self.imagen_png)
                cv2.imshow("Alerta", cv_img)
                #
            if len(comparacion) == 6:
                self.opcion.set(2)
                self.entryPlaca.insert(0, self.placa_var)
                self.comboMarca.set(self.marca_var)
                self.comboModelo.set(self.modelo_var)
                self.comboColor.set(self.color_var)
                
                self.imagen_png = f"D:\Aplicaciones\Yolo_v4\yolov4-custom-functions\detections\\archivosTxtOCR\\{self.archivo_png}"
                cv_img = cv2.imread(self.imagen_png)
                cv2.imshow("Alerta", cv_img)
        #cv2.waitKey(0)

    def upload_to_aws(self):
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id='AKIAZ56RHXMENRCBKN5H',
            aws_secret_access_key='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'
        )

        path = self.imagen_png

        s3.Bucket('reporte-alerta-guardado').upload_file(Filename=path, Key=self.placa_var)

        folder = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #Elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

  
args = ""
MonitoreaCamara(args)