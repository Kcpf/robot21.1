#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

def segmenta_linha_branca(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem e segmentar as faixas brancas
    """
    img = bgr.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    gray[gray > 250] = 255
    gray[gray < 250] = 0
    
    return gray
    
def estimar_linha_nas_faixas(img, mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retorna dois pontos que formen APENAS uma linha em cada faixa. Desenhe cada uma dessas linhas na iamgem.
         formato: [[(x1,y1),(x2,y2)], [(x1,y1),(x2,y2)]]
    """
    lines = cv2.HoughLinesP(mask, 1, math.pi/180, 100, 1000, 50)
    x0_pos,y0_pos = (0,0)
    xf_pos,yf_pos = (0,0)

    x0_neg,y0_neg = (0,0)
    xf_neg,yf_neg = (0,0)
    
    for line in lines:
        dx = line[0][2] - line[0][0]
        dy = line[0][3] - line[0][1]
        coef_angular = dy/dx
        
        if coef_angular > 0:
            x0_pos,y0_pos = line[0][0:2]
            xf_pos,yf_pos = line[0][2:4]
        if coef_angular < 0:
            x0_neg,y0_neg = line[0][0:2]
            xf_neg,yf_neg = line[0][2:4]
    
   
            
    pr1_0 = (x0_pos, y0_pos)
    pr1_f = (xf_pos, yf_pos)

    pr2_0 = (x0_neg, y0_neg)
    pr2_f = (xf_neg, yf_neg)
    
    equacoes = calcular_equacao_das_retas([pr1_0,pr1_f,pr2_0,pr2_f])
    _, pontof = calcular_ponto_de_fuga(img, equacoes)
    
    cv2.line(mask,pr1_0,pontof, (0,0,255),10)
    cv2.line(mask,pr2_0,pontof, (0,0,255),10)
    
    cv2.line(img,pr1_0,pontof, (0,0,255),10)
    cv2.line(img,pr2_f,pontof, (0,0,255),10)
    
    return [pr1_0,pr1_f,pr2_0,pr2_f]

def calcular_equacao_das_retas(linhas):
    """Não mude ou renomeie esta função
        deve receber dois pontos que estejam em cada uma das faixas e retornar a equacao das duas retas. Onde y = h + m * x. Formato: [(m1,h1), (m2,h2)]
    """
    coef1 = (linhas[3][1] - linhas[2][1])/(linhas[3][0] - linhas[2][0])
    coef2 = (linhas[1][1] - linhas[0][1])/(linhas[1][0] - linhas[0][0])
    
    b1 = linhas[2][1] - (coef1*linhas[2][0])
    b2 = linhas[0][1] - (coef2*linhas[0][0])

    return [(coef1, b1), (coef2, b2)]

def calcular_ponto_de_fuga(img, equacoes):
    """Não mude ou renomeie esta função
        deve receber duas equacoes de retas e retornar o ponto de encontro entre elas. Desenhe esse ponto na imagem.
    """
    x = int((equacoes[1][1]-equacoes[0][1])/(equacoes[0][0]-equacoes[1][0]))
    y = int((equacoes[0][0]*x) + equacoes[0][1])
    
    ponto = (x,y)
    cv2.circle(img, ponto, 15, (0,0,255), 2)
    
    return img, ponto

        