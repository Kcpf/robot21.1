#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# Rodar com 
# roslaunch my_simulation rampa.launch


from __future__ import print_function, division
import rospy
import numpy as np
import numpy
import tf
import math
import cv2
import time
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from numpy import linalg
from tf import transformations
from tf import TransformerROS
import tf2_ros
from geometry_msgs.msg import Twist, Vector3, Pose, Vector3Stamped

from nav_msgs.msg import Odometry
from std_msgs.msg import Header


import visao_module


bridge = CvBridge()

cv_image = None
media = []
centro = []

area = 0.0 # Variavel com a area do maior contorno

resultados = [] # Criacao de uma variavel global para guardar os resultados vistos

x = 0
y = 0
z = 0 
id = 0

frame = "camera_link"
# frame = "head_camera"  # DESCOMENTE para usar com webcam USB via roslaunch tag_tracking usbcam
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
    minLineLength = 1000
    maxLineGap = 50
    lines = cv2.HoughLinesP(mask,1,np.pi/180,100,minLineLength,maxLineGap) 
    for line in lines:
        x1, y1, x2, y2 = line[0]
        coef = (y2-y1)/(x2-x1)
        coeflist.append(coef)
    direita = coeflist.index(max(coeflist))
    esquerda = coeflist.index(min(coeflist))
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

def processa(cv_img):
    img = cv_img.copy()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Segmenta parede
    jade_rgb = np.uint8([[[1, 166, 111]]])
    jade_hsv = cv2.cvtColor(jade_rgb, cv2.COLOR_RGB2HSV)

    hsv1 = np.array([jade_hsv[0][0][0] - 20, jade_hsv[0][0][1] - 80, jade_hsv[0][0][2] - 80])

    hsv2 = np.array([jade_hsv[0][0][0] + 20, jade_hsv[0][0][1], jade_hsv[0][0][2]])

    mask = cv2.inRange(img_hsv, hsv1, hsv2)

    cv2.imshow("Mask", mask)
    
    # Calcula Linha
    linhas, img2 = estimar_linha_nas_faixas(cv_img.copy(), mask)
    cv2.imshow("Calcula Linha", cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

    # Calcula Equacoes
    equacoes = calcular_equacao_das_retas(linhas)

    # Estima ponto de fuga
    img, pontof = calcular_ponto_de_fuga(img2, equacoes)
    cv2.imshow("Estima Ponto de fuga", cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    print("frame")
    global cv_image
    global media
    global centro
    global resultados

    now = rospy.get_rostime()
    imgtime = imagem.header.stamp
    lag = now-imgtime # calcula o lag
    delay = lag.nsecs

    try:
        temp_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        cv_image = temp_image.copy()
        cv2.imshow("cv_image", cv_image)
        processa(cv_image)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print('ex', e)
    
if __name__=="__main__":
    rospy.init_node("Q3")

    topico_imagem = "/camera/image/compressed"

    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)

    print("Usando ", topico_imagem)

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

    tolerancia = 25

    try:
        # Inicializando - por default gira no sentido anti-horário
        # vel = Twist(Vector3(0,0,0), Vector3(0,0,math.pi/10.0))
        
        while not rospy.is_shutdown():
            for r in resultados:
                print(r)
            #velocidade_saida.publish(vel)

            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")


