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


def realca_caixa_vermelha(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr
        e fazer alguma filtragem / seleção de modo a obter uma imagem
        de saída grayscale
        em que somente os pixels da caixa estão brancos e todo o restante está vermelho
        Dica: Use mais de um canal, por exemplo R e B
    """
    res = bgr.copy()
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    res[res[:,:,0] < 210] = [0, 0, 0]
    res[res[:,:,2] > 24] = [0, 0, 0]
    res[res[:,:,0] > 0] = [255, 255, 255]
    res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
    return res


if __name__ == "__main__":
    img = cv2.imread("cena_canto_sala.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    saida = realca_caixa_vermelha(img)
    cv2.imwrite( "saida_ex2.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('saida', saida)

    cv2.waitKey(0)

