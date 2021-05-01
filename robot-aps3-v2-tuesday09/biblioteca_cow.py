#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import os



def load_mobilenet():
    """Não mude ou renomeie esta função
        Carrega o modelo e os parametros da MobileNet. Retorna a classe da rede.
    """
    proto = "./mobilenet_detection/MobileNetSSD_deploy.prototxt.txt" # descreve a arquitetura da rede
    model = "./mobilenet_detection/MobileNetSSD_deploy.caffemodel" # contém os pesos da rede em si

    net = cv2.dnn.readNetFromCaffe(proto, model)

    return net

def detect(net, frame, CONFIDENCE, COLORS, CLASSES):
    """
        Recebe - uma imagem colorida BGR
        Devolve: objeto encontrado
    """
    """
        Recebe - uma imagem colorida BGR
        Devolve: objeto encontrado
    """
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    results = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence


        if confidence > CONFIDENCE:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY) ))
    # show the output image
    return image, results


def separar_caixa_entre_animais(img, resultados):
    """Não mude ou renomeie esta função
        recebe o resultados da MobileNet e retorna dicionario com duas chaves, 'vaca' e 'lobo'.
        Na chave 'vaca' tem uma lista de cada caixa que existe uma vaca, no formato: [ [min_X, min_Y, max_X, max_Y] , [min_X, min_Y, max_X, max_Y] ]. Desenhe um azul em cada vaca
        Na chave 'lobo' tem uma lista de uma unica caixa que engloba todos os lobos da imagem, no formato: [min_X, min_Y, max_X, max_Y]. Desenhe um vermelho sobre os lobos

    """
    contorno = img.copy()

    animais = {}
    animais['vaca'] = []
    animais['lobo'] = []

    for array in resultados:
        if array[0] == 'cow':
            coord = [array[2][0], array[2][1], array[3][0], array[3][1]]
            animais['vaca'].append(coord)

        elif array[0] == 'dog' or 'sheep' or 'horse':
            coord = [array[2][0], array[2][1], array[3][0], array[3][1]]
            animais['lobo'].append(coord)
    vaca = animais['vaca']
    lobo = animais['lobo']
    minx, miny, maxx, maxy = 7000, 7000, 0, 0
    cordLobo = [minx,miny,maxx,maxy]

    for vaca in vaca:
        cv2.rectangle(contorno, (vaca[0], vaca[1]), (vaca[2], vaca[3]), (255,0,0), 6)
    for lobo in lobo:
        if lobo[0] < minx:
            minx = lobo[0]
        if lobo[1] < miny:
            miny = lobo[1]
        if lobo[2] > maxx:
            maxx = lobo[2]
        if lobo[3] > maxy:
            maxy = lobo[3]
    cordLobo = [minx,miny,maxx,maxy]

    
        
    cv2.rectangle(contorno, (minx, miny), (maxx, maxy), (0,0,255), 6)

    return contorno, animais

def calcula_iou(boxA, boxB):

	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def checar_perigo(image, animais):
    """Não mude ou renomeie esta função
        Recebe as coordenadas das caixas, se a caixa de uma vaca tem intersecção com as do lobo, ela esta em perigo.
        Se estiver em perigo, deve escrever na imagem com a cor vermlha, se não, escreva com a cor azul.
        
        Repita para cada vaca na imagem.
    """
    vaca = animais['vaca']
    lobo = animais['lobo']
    minx, miny, maxx, maxy = 7000, 7000, 0, 0

    for lobo in lobo:
        if lobo[0] < minx:
            minx = lobo[0]
        if lobo[1] < miny:
            miny = lobo[1]
        if lobo[2] > maxx:
            maxx = lobo[2]
        if lobo[3] > maxy:
            maxy = lobo[3]
    cordLobo = [minx,miny,maxx,maxy]

    for vaca in vaca:
        
        iou = calcula_iou(vaca,cordLobo)
        
        if iou > 0.05:
            cv2.putText(image, str('Vaca em perigo !!!'), (vaca[0],vaca[1]), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)
        
        else:
            cv2.putText(image, str('Vaca segura'), (vaca[0],vaca[1]), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)






    
    return image