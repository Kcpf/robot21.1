#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import print_function, division


# Sugerimos rodar com:
#         roslaunch turtlebot3_gazebo rampa.launch
import rospy

import numpy as np

import cv2

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry

import math


ranges = None
minv = 0
maxv = 10
cv_image = None

bridge = CvBridge()

estagio1 = True
contador_estagio1 = 0
maior_contorno = 0
angulo_maior_contorno = 0
estagio2 = False

def processa(contador_estagio1):
    global maior_contorno
    global angulo_maior_contorno

    img = cv_image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv1 = np.array([135,  50,  50])
    hsv2 = np.array([170, 255, 255])

    mask = cv2.inRange(img,  hsv1, hsv2)

    # cv2.imshow("mask", mask)

    contornos, arvore = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    maior = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c
    
    if maior_area > maior_contorno:
        print(maior_area, maior_contorno)
        maior_contorno = maior_area
        angulo_maior_contorno = contador_estagio1

def recebeu_leitura(dado):
	print(dado)


def scaneou(dado):
    global ranges
    global minv
    global maxv
    print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    ranges = np.array(dado.ranges).round(decimals=2)
    minv = dado.range_min 
    maxv = dado.range_max
 
# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    global cv_image
    # print("frame")
    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        cv2.imshow("Camera", cv_image)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print('ex', e)

if __name__=="__main__":

    rospy.init_node("q4")
    sleep_time = 0.1

    topico_imagem = "/camera/image/compressed"
    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
    recebe_odom = rospy.Subscriber("/odom", Odometry , recebeu_leitura)
    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)

    rospy.sleep(1)
    while not rospy.is_shutdown():

        if estagio1:
            vel = Twist(Vector3(0,0,0), Vector3(0,0,math.pi/16))

            velocidade_saida.publish(vel)
            rospy.sleep(sleep_time)
            contador_estagio1 += 1
            
            processa(contador_estagio1)

            if contador_estagio1 == 165:
                estagio1 = False
                estagio2 = True
        
        if estagio2:
            print(angulo_maior_contorno)
            sleep_time = 0.1
            vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
            velocidade_saida.publish(vel)
        
        rospy.sleep(sleep_time)



