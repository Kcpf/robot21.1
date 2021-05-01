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
files = "chess01.png chess02.png chess03.png chess04.png".split()

nd = " " # vazio

# Lista vazia para ser tabuleiro
board = [[nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd]]

# Só teremos reis e peões e o tabuleiro é 5x5 somente
rei_preto = "BK" # black king
peao_preto = "BP"  # black pawn
rei_branco = "WK" # white king
peao_branco = "WP" # white pawn

def verifica_quadrado(quadrado):
    # Verifica Branco
    q = quadrado.copy()
    q = cv2.cvtColor(quadrado, cv2.COLOR_BGR2HSV)

    hsv1 = np.array([ 0, 0, 200])

    hsv2 = np.array([ 5, 10, 255])

    mask = cv2.inRange(q, hsv1, hsv2)
    contador_branco = len(np.where(mask == 255)[0])

    # cv2.imshow('q', mask)

    # Verifica Preto
    q = quadrado.copy()
    q = cv2.cvtColor(quadrado, cv2.COLOR_BGR2HSV)

    hsv1 = np.array([ 0, 0, 0])

    hsv2 = np.array([ 5, 10, 5])

    mask = cv2.inRange(q, hsv1, hsv2)

    # cv2.imshow('q', mask)
    contador_preto = len(np.where(mask == 255)[0])

    # Verifica qual a peca
    # print(f"ContadorBranco: {contador_branco} \nContadorPreto: {contador_preto}")

    if contador_preto == 0 and contador_branco == 0:
        return None

    if contador_preto > contador_branco:
        if contador_branco > 400:
            return "BK"
        else:
            return "BP"
    else:
        if contador_preto > 700:
            return "WK"
        else:
            return "WP"
    


# Trabalhe nesta função
# Pode criar e chamar novas funções o quanto quiser
def processa(frame_bgr): 
    img = frame_bgr.copy()
    tabuleiro = [[nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd], [nd,nd,nd,nd,nd]]
    quadrados = [
        [img[: (465//5), : (465//5)], img[: (465//5), (465//5):(465//5)*2], img[: (465//5), (465//5)*2 : (465//5)*3], img[: (465//5), (465//5)*3 : (465//5)*4], img[: (465//5), (465//5)*4 : 465]],
        [img[(465//5): (465//5)*2, : (465//5)], img[(465//5): (465//5)*2, (465//5):(465//5)*2], img[(465//5): (465//5)*2, (465//5)*2 : (465//5)*3], img[(465//5): (465//5)*2, (465//5)*3 : (465//5)*4], img[(465//5): (465//5)*2, (465//5)*4 : 465]],
        [img[(465//5)*2: (465//5)*3, : (465//5)], img[(465//5)*2: (465//5)*3, (465//5):(465//5)*2], img[(465//5)*2: (465//5)*3, (465//5)*2 : (465//5)*3], img[(465//5)*2: (465//5)*3, (465//5)*3 : (465//5)*4], img[(465//5)*2: (465//5)*3, (465//5)*4 : 465]],
        [img[(465//5)*3: (465//5)*4, : (465//5)], img[(465//5)*3: (465//5)*4, (465//5):(465//5)*2], img[(465//5)*3: (465//5)*4, (465//5)*2 : (465//5)*3], img[(465//5)*3: (465//5)*4, (465//5)*3 : (465//5)*4], img[(465//5)*3: (465//5)*4, (465//5)*4 : 465]],
        [img[(465//5)*4: 465, : (465//5)], img[(465//5)*4: 465, (465//5):(465//5)*2], img[(465//5)*4: 465, (465//5)*2 : (465//5)*3], img[(465//5)*4: 465, (465//5)*3 : (465//5)*4], img[(465//5)*4: 465, (465//5)*4 : 465]]
    ]

    
    for i, linha in enumerate(quadrados):
        for j, quadrado in enumerate(linha):
            resposta = verifica_quadrado(quadrado)
            if resposta != None:
                tabuleiro[i][j] = resposta

    # Este código é só exemplo da lógica 
    # Use a notação linha x coluna
    # Seu código deve retornar o tabuleiro e uma imagem 
    # que demonstre alguma saída visual
    return tabuleiro, img



if __name__ == "__main__":

    # Inicializa a leitura dos arquivos
    bgr = [cv2.imread(f) for f in files]
    
    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    for frame in bgr: 
        # Capture frame-by-frame

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Você vai trabalhar na função processa!
        tabuleiro, imagem = processa(frame)

        print("Tabuleiro")
        print(np.array(tabuleiro))

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem processada', imagem)

        if cv2.waitKey(1500) & 0xFF == ord('q'):
            break



