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
video = "bandeiras_movie.mp4"

corner_jp = ((10,10),(100,100))
corner_pl = ((5,5),(200,200))

font = cv2.FONT_HERSHEY_SIMPLEX

def texto(img, a, p, rgb=(0,50,100)):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font,1,rgb,2,cv2.LINE_AA)

# Responda dentro desta função. 
# Pode criar e chamar novas funções o quanto quiser
def encontra_japao_polonia_devolve_corners(bgr):
    frame = bgr.copy()
    # Encontra maior quadrado branco (Japao)
    jp = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv1 = np.array([ 0, 0, 200])

    hsv2 = np.array([ 5, 10, 255])

    mask = cv2.inRange(jp, hsv1, hsv2)

    segmentado = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((4, 4)))

    contornos, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    maior = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c

    # cv2.drawContours(frame, [maior], -1, [0, 0, 255], 3)
    x,y,w,h = cv2.boundingRect(maior)
    
    corner_jp = ((x, y), (x + w, y + h))
    cv2.rectangle(frame, corner_jp[0], corner_jp[1], (255, 0,0), 4)

    # cv2.circle(frame, (x,y), radius=10, color=(255, 0,0), thickness=-1)
    # cv2.circle(frame, (x + w, y + h), radius=10, color=(255, 0,0), thickness=-1)

    texto(frame, "Japao", (x, y+h+30), rgb=(255,0,0))

    # Encontra segundo maior quadrado branco e maior quadrado vermelho (Polonia)

    pl = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv1 = np.array([159,  50,  50])

    hsv2 = np.array([194, 255, 255])

    mask = cv2.inRange(pl, hsv1, hsv2)

    segmentado = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((4, 4)))

    contornos, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    maior = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c

    x,y,w,h = cv2.boundingRect(maior)
    # cv2.drawContours(frame, [maior[-2]], -1, [0, 0, 255], 3)
    
    corner_pl = ((x, y-h), (x + w, y + h))
    cv2.rectangle(frame, corner_pl[0], corner_pl[1], (0, 255,0), 4)

    # cv2.circle(frame, (x, y-h), radius=10, color=(0, 255,0), thickness=-1)
    # cv2.circle(frame, (x + w, y + h), radius=10, color=(0, 255,0), thickness=-1)

    texto(frame, "Polonia", (x, y+h+30), rgb=(0,255,0))

    return frame, corner_jp, corner_pl



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

        # Programe só na função encontra_japao_devolve_corners. Pode criar funções se quiser
        saida, japao, polonia = encontra_japao_polonia_devolve_corners(frame)

        print("Corners x-y Japao")
        print(japao)
        print("Corners x-y Polonia")
        print(polonia)

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', saida)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


