#from PIL import Image

#import sys
#from pdf2image import convert_from_path
#import os
import cv2
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

#PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

image = cv2.imread('placa1.jpg') #Carga la imagen utilizando opencv
text = pytesseract.image_to_string(image,config='--psm 11') #Extrae el texto de la imagen
print('Texto: ',text) #Muestra el resultado del texto de la imagen

cv2.imshow('Image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()



