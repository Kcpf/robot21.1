#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
# Baixe o arquivo em:
# https://github.com/Insper/robot20/blob/master/media/dominoes.mp4
    
video = "dominoes.mp4"
font = cv2.FONT_HERSHEY_SIMPLEX

def texto(img, a, p, color=(0,255,255), font=font, width=2, size=1):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font,size,color,width,cv2.LINE_AA)

def processa(gray):
    
    img = gray.copy()

    img[img >= 150] = 255
    img[img < 150] = 0

    diff = np.where(img == 255)
    x = sorted(diff[0])
    x_min = x[0]
    x_max = x[-1]

    y = sorted(diff[1])
    y_min = y[0]
    y_max = y[-1]

    img = img[x_min:x_max, y_min:y_max]

    cv2.imshow("Imagem modificada", img)

    gap_meio = 25
    gap_bordas = 10
    meio = int(len(img)/2)
    img_cima = img[gap_bordas : meio - gap_meio, gap_bordas : len(img[0]) - gap_bordas]
    img_baixo = img[meio + gap_meio : len(img) - gap_bordas, gap_bordas : len(img[0]) - gap_bordas]

    kernel = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])
    img_cima = cv2.filter2D(img_cima, -1, kernel)
    img_baixo = cv2.filter2D(img_baixo, -1, kernel)

    cv2.imshow("Imagem cima", img_cima)
    cv2.imshow("Imagem baixo", img_baixo)

    contornos_cima, _ = cv2.findContours(
        img_cima,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contornos_baixo, _ = cv2.findContours(
        img_baixo,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    area_cima = [cv2.contourArea(contorno) for contorno in contornos_cima]
    area_baixo = [cv2.contourArea(contorno) for contorno in contornos_baixo]

    print(area_cima, area_baixo)
    
    return ((len(area_cima) - 1) // 2, (len(area_baixo) - 1) // 2)
    


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        contador_cima, contador_baixo = processa(gray)
        texto(frame, f"{contador_cima} por {contador_baixo}", (50, 50))

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


