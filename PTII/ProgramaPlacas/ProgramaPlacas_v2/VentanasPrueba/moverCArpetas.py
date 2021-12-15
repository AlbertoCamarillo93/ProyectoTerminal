import shutil
import os
"""
MUEVE ARCHIVOS A OTRA CARPETA
n = 1

source = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\crop\\00010\\frame_0'#\\PlacaVehicular_1.png'

#shutil.move(source,destination)

files = os.listdir(source)

for file in files:
    destination = f'D:\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR\\PlacaVehicular_{n}.png'
    new_path = shutil.move(f"{source}/{file}", destination)
    n += 1 
    print(new_path)
"""
"""
RECORRE LAS SUBCARPETAS DE UNA CARPETA, BUSCANDO LOS ARCHIVOS EXISTENTES
m = 0
rootDir = f'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\crop\\00010'#\\frame_{m}'
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
    print('Directorio encontrado: %s' % dirName)
    m += 50
    for fname in fileList:
        print('\t%s' % fname)
    rootDir = f'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\crop\\00010\\frame_{m}'
"""

n = 1
m = 0
rootDir = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\crop\\00010'#\\frame_{m}'#\\PlacaVehicular_1.png'

files = os.listdir(rootDir)
for dirName, subdirList, files in os.walk(rootDir, topdown=False):
    print('Directorio encontrado: %s' % dirName)
    m += 50
    for file in files:
        destination = f'D:\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR\\PlacaVehicular_{n}.png'
        new_path = shutil.move(f"{dirName}/{file}", destination)
        n += 1 
        print(new_path)