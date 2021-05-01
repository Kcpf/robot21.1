#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division

import cv2
import os
import sys
import os.path
import numpy as np
import math


def encontrar_foco(D, H, h):
    """Não mude ou renomeie esta função
        deve receber respectivamente a distancia real, o a distancia real entre os circulos e a distancia na image entre os circulos e deve retornar o foco
    """
    f = (D*h)/H
    return f


def segmenta_circulo_ciano(hsv):
    """Não mude ou renomeie esta função
        deve receber uma imagem em hsv e devolver uma nova imagem com tudo em preto e os pixels do circulos ciano em branco
    """
    hsv1 = np.array([85, 150, 150])
    hsv2 = np.array([95, 255, 255])
    mask = cv2.inRange(hsv, hsv1, hsv2)

    return mask


def segmenta_circulo_magenta(hsv):
    """Não mude ou renomeie esta função
        deve receber uma imagem em hsv e devolver uma nova imagem com tudo em preto e os pixels do circulos magenta em branco
    """
    hsv1 = np.array([145, 150, 150])
    hsv2 = np.array([155, 255, 255])
    mask = cv2.inRange(hsv, hsv1, hsv2)
    return mask


def encontrar_maior_contorno(segmentado):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retornar APENAS o maior contorno obtido
    """
    contornos, arvore = cv2.findContours(
        segmentado.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    maior = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c

    return maior


def encontrar_centro_contorno(contorno):
    """Não mude ou renomeie esta função
        deve receber um contorno e retornar o centro dele, formato: (XX, YY)
    """
    M = cv2.moments(contorno)

    if (M["m00"] == 0):
        return (0, 0)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (int(cX), int(cY))


def calcular_h(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
        deve receber dois pontos e retornar a distancia absoluta entre eles
    """
    x1, y1 = centro_ciano
    x2, y2 = centro_magenta

    h = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return int(h)


def encontrar_circulos(bgr):
    """retorna os círculsos encontrados na imagem 
    No formato (x,y,raio)
    """

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    sigma = 0.33

    v = np.median(gray)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    bordas = cv2.Canny(gray, lower, upper)

    circles = cv2.HoughCircles(bordas, cv2.HOUGH_GRADIENT, 2,
                               40, param1=50, param2=100, minRadius=5, maxRadius=120)

    circles = np.uint16(np.around(circles))

    return circles


def encontrar_distancia(f, H, h):
    """Não mude ou renomeie esta função
        deve receber respectivamente o foco a distancia real entre os circulos e a distancia na image entre os circulos e retornar a distancia real
    """
    if h == 0:
        return 0

    D = (f*H)/h
    return D


def calcular_distancia_entre_circulos(img):
    """Não mude ou renomeie esta função
        deve utilizar as funções acima para retornar a distancia entre os circulos, o centro_ciano, o centro_magenta e a imagem com os contornos desenhados
    """
    contornos_img = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    segmentado_ciano = segmenta_circulo_ciano(hsv)
    segmentado_magenta = segmenta_circulo_magenta(hsv)

    contorno_ciano = encontrar_maior_contorno(segmentado_ciano)
    contorno_magenta = encontrar_maior_contorno(segmentado_magenta)

    centro_ciano = encontrar_centro_contorno(contorno_ciano)
    centro_magenta = encontrar_centro_contorno(contorno_magenta)

    h = calcular_h(centro_ciano, centro_magenta)

    return h, centro_ciano, centro_magenta, contornos_img


def calcular_angulo_com_horinzontal_da_imagem(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
        deve calcular o angulo, em radiano, entre o vetor formato com os centros do circulos e a horizontal.
        Retornar o angulo em graos
    """
    x1, y1 = centro_ciano
    x2, y2 = centro_magenta

    h = calcular_h(centro_ciano, centro_magenta)

    if h == 0:
        return 0

    angulo = math.degrees(math.acos((x1-x2)/h))

    return angulo
