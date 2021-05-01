#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

import cv2
import os
import sys
import os.path
import numpy as np
import fotogrametria

# ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-

font = cv2.FONT_HERSHEY_SIMPLEX


def texto(img, a, p, color=(0, 255, 255), font=font, width=2, size=1):
    """Escreve na img RGB dada a string a na posição definida pela tupla p"""
    cv2.putText(img, str(a), p, font, size, color, width, cv2.LINE_AA)


def calcular_e_desenhar_na_image_da_webcam(img):
    """Não mude ou renomeie esta função
        ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems com os contornos desenhados e a distancia e o angulo escrito em um canto da imagem.
    """
    # O foco deve ser adaptado dependendo da câmera do computador que esta usando
    f = fotogrametria.encontrar_foco(40, 7.6, 100)

    h, centro_ciano, centro_magenta, contornos_img = fotogrametria.calcular_distancia_entre_circulos(
        img)

    # Desenhando Contorno
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    segmentado_ciano = fotogrametria.segmenta_circulo_ciano(hsv)
    segmentado_magenta = fotogrametria.segmenta_circulo_magenta(hsv)

    # Ciano
    contorno_ciano = fotogrametria.encontrar_maior_contorno(segmentado_ciano)
    if contorno_ciano is not None:
        cv2.drawContours(img, [contorno_ciano], -1, [0, 0, 255], 3)

    # Magenta
    contorno_magenta = fotogrametria.encontrar_maior_contorno(
        segmentado_magenta)

    if contorno_magenta is not None:
        cv2.drawContours(img, [contorno_magenta], -1, [255, 0, 0], 3)

    # Desenhando Linha ligando centros
    centro_ciano = fotogrametria.encontrar_centro_contorno(contorno_ciano)
    centro_magenta = fotogrametria.encontrar_centro_contorno(contorno_magenta)

    cv2.line(img, centro_ciano, centro_magenta,
             (0, 255, 0), thickness=3, lineType=8)

    d = fotogrametria.encontrar_distancia(f, 12.70, h)

    angulo = fotogrametria.calcular_angulo_com_horinzontal_da_imagem(
        centro_ciano, centro_magenta)

    # Escrever informações na tela

    texto(img, f"Distance: {d:.2f}cm", (50, 50), color=(0, 255, 0))
    texto(img, f"Angle: {angulo:.2f} degrees", (50, 100), color=(0, 255, 0))

    return img


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    img = calcular_e_desenhar_na_image_da_webcam(frame)
    cv2.imshow("preview", img)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
