#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import biblioteca as bib
from sklearn.linear_model import LinearRegression
from scipy import stats

print("Baixe o arquivo a seguir para funcionar: ")
print("https://github.com/Insper/robot202/raw/master/projeto/centro_massa/video.mp4")

cap = cv2.VideoCapture('line_following.mp4')

#texto para aparecer o angulo
font = cv2.FONT_HERSHEY_SIMPLEX
def texto(img, a, p, color=(0,255,255), font=font, width=2, size=1 ):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font,size,color,width,cv2.LINE_AA)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    # frame = cv2.imread("frame0000.jpg")
    # ret = True

    segmenta = None
    mask = img.copy()
    segmenta = bib.segmenta_linha_amarela(mask)
    angulo = None


    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")
        break
    else:
        if segmenta is not None:
            contornos = bib.encontrar_contornos(segmenta)
            cv2.drawContours(mask, contornos,-1, [0, 0, 255], 2)
            
            mask, x, y = bib.encontrar_centro_dos_contornos(mask, contornos) 
    
            
            mask = bib.desenhar_linha_entre_pontos(mask, x, y,(255,0,0)) 
                
            slope, intercept, r, p, std_err = stats.linregress(x, y)

            ponto1 = (img.shape[1], int(slope * img.shape[1] + intercept))
            ponto2 = (0, int(slope * 0 + intercept))

            cv2.line(mask, ponto1, ponto2, (0, 255, 0), 5)
            lm = [slope, intercept]
            angulo = bib.calcular_angulo_com_vertical(mask, lm)
            
            
            
        else:
            pass
    texto(mask, "Angulo: " + str(angulo), (50, 80) )



            


    # Imagem original
    cv2.imshow('img',img)
    # Mascara
    cv2.imshow('mask',mask)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

