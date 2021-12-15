# test file if you want to quickly try tesseract on a license plate image
import re
import shutil
import pytesseract
import cv2
import os

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
def OCR():
    imagenes_path = 'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\leeOCR'
    imagenes = os.listdir(imagenes_path)
    print(imagenes)

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
        cv2.imshow("Otsu", thresh)
        cv2.waitKey(0)
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

        # apply dilation 
        dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
        cv2.imshow("dilation", dilation)
        cv2.waitKey(0)
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
            #cv2.imshow("ROI", roi)
            #cv2.waitKey(0)
            text = pytesseract.image_to_string(roi, config='-c tessedit_char_whitelist=-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 13 --oem 3')#8 --oem 3')
            #print(text)
            plate_num += text
            plate_num = re.sub(r'[^\da-zA-Z]+', '', plate_num) #Permite solo caracteres alfanumericos, los demas los elimina. 
        
        if len(plate_num) < 5:
            continue
        else:     
            file = open(f"D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR\\ocrDetect{n}.txt", "wb")
            file.write(plate_num.encode())# + os.linesep)
            destination = f'D:\\Aplicaciones\\Yolo_v4\\yolov4-custom-functions\\detections\\archivosTxtOCR\\ocrDetect{n}.png'
            new_path = shutil.move(f"{imagenes_path}/{imagen}", destination)
            print("placa:", plate_num)
            n += 1

#cv2.imshow("Character's Segmented", im2)
#cv2.waitKey(0)
#cv2.destroyAllWindows()