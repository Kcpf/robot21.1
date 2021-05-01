#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist, Vector3

v = 0.1  # Velocidade linear
w = math.pi/16  # Velocidade Angular

if __name__ == "__main__":
    rospy.init_node("roda_exemplo")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)
    rospy.sleep(3.0)

    try:
        while not rospy.is_shutdown():

            vel = Twist(Vector3(v,0,0), Vector3(0,0,0))
            pub.publish(vel)
            rospy.sleep(5.0)

            vel = Twist(Vector3(0,0,0), Vector3(0,0,w))
            pub.publish(vel)
            rospy.sleep(8.0)
            
    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
