#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def segmenta_linha_branca(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem e segmentar as faixas brancas
    """    
    gray = bgr.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray[gray > 240] = 255
    gray[gray < 240] = 0

    return gray


def estimar_linha_nas_faixas(img, mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retorna dois pontos que formen APENAS uma linha em cada faixa. Desenhe cada uma dessas linhas na iamgem.
         formato: [[(x1,y1),(x2,y2)], [(x1,y1),(x2,y2)]]
    """

    x5 = 0
    x6 = 0
    y5 = 0
    y6 = 0
    x3 = 0
    y3 = 0
    x4 = 0
    y4 = 0
    coeflist = []
    linhas = [[(x5,y5),(x6,y6)], [(x3,y3),(x4,y4)]]
    coeflist
    minLineLength = 1000
    maxLineGap = 50
    lines = cv2.HoughLinesP(mask,1,np.pi/180,100,minLineLength,maxLineGap) 
    for line in lines:
        x1, y1, x2, y2 = line[0]
        coef = (y2-y1)/(x2-x1)
        coeflist.append(coef)
    direita = coeflist.index(min(coeflist))
    esquerda = coeflist.index(max(coeflist))
    x5, y5, x6, y6 = lines[direita][0][0], lines[direita][0][1], lines[direita][0][2], lines[direita][0][3]
    x3, y3, x4, y4 = lines[esquerda][0][0], lines[esquerda][0][1], lines[esquerda][0][2], lines[esquerda][0][3]   
    linhas = [[(x5,y5),(x6,y6)], [(x3,y3),(x4,y4)]]
    comeco = (x5,y5)
    fim = (x6,y6)
    comeco2 = (x3,y3)
    fim2 = (x4,y4)
    cv2.line(img,comeco, fim, (255, 0, 255), thickness=3, lineType=8)
    cv2.line(img,comeco2, fim2, (255, 0, 255), thickness=3, lineType=8)

    return linhas, img


            
        
        


def calcular_equacao_das_retas(linhas):
    """Não mude ou renomeie esta função
        deve receber dois pontos que estejam em cada uma das faixas e retornar a equacao das duas retas. Onde y = h + m * x. Formato: [(m1,h1), (m2,h2)]
    """
    coeficiente = []
    for linha in linhas:
        x5, x6 = linha[0][0],linha [1][0]
        y5, y6 = linha[0][1], linha[1][1]
        m = (y5-y6)/(x5-x6)
        h = y6 - (m*x6)
        coefi = [m,h]
        print(coefi)
        coeficiente.append(coefi)
        
    return coeficiente

def calcular_ponto_de_fuga(img, equacoes):
    """Não mude ou renomeie esta função
        deve receber duas equacoes de retas e retornar o ponto de encontro entre elas. Desenhe esse ponto na imagem.
    """
    
    h1 = equacoes[0][1]
    h2 = equacoes[1][1]
    m1 = equacoes[0][0]
    m2 = equacoes[1][0]
    xi = int((h2-h1)/(m1-m2))
    yi = int((m1*xi) + h1)
    pontoFuga = img.copy()
    
    # Center coordinates
    center_coordinates = (xi, yi)
 
    # Radius of circle
    radius = 10
    
    # Blue color in BGR
    color = (255, 0, 255)
    
    # Line thickness of 2 px
    thickness = -1
    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    cv2.circle(pontoFuga, center_coordinates, radius, color, thickness)


    
    return pontoFuga, (xi,yi)

        