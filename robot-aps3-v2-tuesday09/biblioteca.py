#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

from sklearn.linear_model import LinearRegression
from scipy import stats

def segmenta_linha_amarela(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e retornar os segmentos amarelos do centro da pista em branco.
        Utiliza a função cv2.morphologyEx() para limpar ruidos na imagem
    """
    img_hsv = cv2.cvtColor(bgr.copy(), cv2.COLOR_BGR2HSV)

    hsv1 = np.array([20, 100, 150])
    hsv2 = np.array([35, 255, 255])

    mask = cv2.inRange(img_hsv, hsv1, hsv2)

    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((5, 5)))

    return mask

def encontrar_contornos(mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca os contornos encontrados
    """
    
    
    contornos, arvore = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contornos
    

    

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)

def encontrar_centro_dos_contornos(img, contornos):
    """Não mude ou renomeie esta função
        deve receber um contorno e retornar, respectivamente, a imagem com uma cruz no centro de cada segmento e o centro dele. formato: img, x, y
    """
    img_contornos = img.copy()
    X = []
    Y = []

    for contorno in contornos:
        M = cv2.moments(contorno)
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            point = (int(cX), int(cY))
            crosshair(img_contornos, point, 15, (0, 0, 255))
            X.append(int(cX))
            Y.append(int(cY))
        except:
            pass

    return img_contornos, X, Y

def desenhar_linha_entre_pontos(img, X, Y, color):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e retornar uma imagem com uma linha entre os centros EM SEQUENCIA do mais proximo.
    """
    linha = img.copy()
    for i in range(len(X)-1):
        cv2.line(linha,(X[i],Y[i]),(X[i+1],Y[i+1]),(255, 0, 0), 2)

    return linha

def regressao_por_centro(img, x,y):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta e os parametros da reta

        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    
    value =[]
    j = 0
    while j < len(x):
        a = ((x[j]*x[j]) + (y[j]*y[j]))**(1/2)
        value.append(a)
        j+=1
    # First quartile (Q1) 
    Q1 = np.percentile(value, 25, interpolation = 'midpoint') 
    
    # Third quartile (Q3) 
    Q3 = np.percentile(value, 75, interpolation = 'midpoint') 
    
    # Interquaritle range (IQR) 
    iqr = Q3 - Q1
    filterx = []
    filtery = []
    i=0
    while i < len(value)-1:
        if Q1-(iqr*1.5) <= value[i]:
            if Q3+(iqr*1.5) >= value[i]:
                filterx.append(x[i])
                filtery.append(y[i])
                i += 1
        else: 
            i+=1
        
    regressao = img.copy()
    slope, intercept, r, p, std_err = stats.linregress(filterx, filtery)

    ponto1 = (img.shape[1], int(slope * img.shape[1] + intercept))
    ponto2 = (0, int(slope * 0 + intercept))

    cv2.line(regressao, ponto1, ponto2, (0, 255, 0), 10)

    return regressao, [slope, intercept]

def calcular_angulo_com_vertical(img, lm):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta.

        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    m = lm[0]

    alpha = math.atan(m)
    beta = abs(math.degrees(alpha))
    angulo = 90 - beta

    return angulo
