#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())


def recorta_leopardo(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e devolver uma nova imagem com tudo em preto e o os pixels da caixa em granco
    """
    res = bgr.copy()
    res = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
    
    # Encontrando index de pixels vermelhos 
    vermelho = np.where(res == [255, 0, 0])

    # Contando quantos pixels vermelhos por linha
    unico_linha, contador_linha = np.unique(vermelho[0], return_counts=True)
    ocorrencias_linha = dict(zip(unico_linha, contador_linha))

    # Encontrando linha que possui mais pixels vermelhos
    y_max = max(ocorrencias_linha, key=ocorrencias_linha.get)
    
    # Contando quantos pixels vermelhos por coluna
    unico_coluna, contador_coluna = np.unique(vermelho[1], return_counts=True)
    ocorrencias_coluna = dict(zip(unico_coluna, contador_coluna))

    # Encontrando coluna que possui mais pixels vermelhos
    x_max = max(ocorrencias_coluna, key=ocorrencias_coluna.get)


    # Repetindo processo para o quadrado azul..
    azul = np.where(res == [0, 0, 255])
    unico_linha, contador_linha = np.unique(azul[0], return_counts=True)

    ocorrencias_linha = dict(zip(unico_linha, contador_linha))
    y_min = max(ocorrencias_linha, key=ocorrencias_linha.get)

    unico_coluna, contador_coluna = np.unique(azul[1], return_counts=True)

    ocorrencias_coluna = dict(zip(unico_coluna, contador_coluna))
    x_min = max(ocorrencias_coluna, key=ocorrencias_coluna.get)

    # Recortando imagem
    res = res[y_min: y_max,x_min: x_max]

    res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
    return res


if __name__ == "__main__":
    img = cv2.imread("snowleopard_red_blue_600_400.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    saida = recorta_leopardo(img)
    cv2.imwrite("ex3_recorte_leopardo.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('saida', saida)

    cv2.waitKey(0)

