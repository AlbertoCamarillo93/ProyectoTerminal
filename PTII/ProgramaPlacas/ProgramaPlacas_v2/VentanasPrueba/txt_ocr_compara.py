import json
import re
import os 
""""""
#Bloque que lee el archivo JSON y lo almacena en una lista
file_json = open("D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\ProyectoTerminal\\ProgramaPlacas_v2\\PlacasReporteBusqueda.json", "r")
content_json =  file_json.read()
jsondecoded = json.loads(content_json)
lista_Placa_json = []
for plates in jsondecoded ["Automoviles"]:
    placa_auto = plates["Placa"]
    placa_auto = re.sub(r'[^\da-zA-Z]+', '', placa_auto)
    lista_Placa_json.append(placa_auto)
    #print("Placa:", placa_auto)#Imprime cada placa 

print("Lista de placas en JSON: ", lista_Placa_json)


#Bloque que lee el archivo txt y guarda cada linea del texto como un elemento dentro de una lista
txt_path = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR'
txt_files = os.listdir(txt_path)

lista_Placa_txt = []
#lista_archivos_txt = []
lista_archivos_png = []
for txt_file in txt_files:
    if txt_file.endswith(".txt"):
        #print(txt_file)
        #lista_archivos_txt.append(txt_file)
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
        lista_archivos_png.append(txt_file)
                 
print("Lista de placas en txt: ", lista_Placa_txt)
print("Lista de archivos PNG: ", lista_archivos_png)
#print("Lista de archivos TXT: ", lista_archivos_txt)

#Bloque para comparar las dos cadenas
i = 0
listaCompara_OcrTxt = []
for atxt in lista_Placa_txt:
    
    for aJson in lista_Placa_json:
        if atxt in aJson:
            listaCompara_OcrTxt.append(aJson)

            archivo_png = lista_archivos_png[i]
            print("lista_archivos_png.index(i)", archivo_png)

    i += 1
listaCompara_OcrTxt_actualizada = []
for item in listaCompara_OcrTxt:
    if item not in listaCompara_OcrTxt_actualizada:
        listaCompara_OcrTxt_actualizada.append(item)
        

            
print("listaCompara_OcrTxt: ",listaCompara_OcrTxt)
print("listaCompara_OcrTxt: ",listaCompara_OcrTxt_actualizada)


#Regresa todos los valores de la placa detectada, recorriendo de nuevo el Json
for x in listaCompara_OcrTxt_actualizada:
    for plates1 in jsondecoded ["Automoviles"]:
        placa_auto1 = plates1["Placa"]
        placa_auto1 = re.sub(r'[^\da-zA-Z]+', '', placa_auto1)
        if placa_auto1 == x:
            print("Placa:", plates1["Placa"])
            #print("Marca:", plates1["Marca"])
            #print("Modelo:", plates1["Modelo"])
            #print("Color:", plates1["Color"])