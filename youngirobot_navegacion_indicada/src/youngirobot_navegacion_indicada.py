#!  /usr/bin/env python

import rospy
import actionlib
from punto import Punto
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult



def mover_robot_a_punto(punto):

    rospy.init_node('youngirobot_navegacion_indicada')

    rate = rospy.Rate(2)
    move = MoveBaseGoal()

    move.target_pose.header.frame_id = 'map'
    move.target_pose.pose.position.x = punto.get_posicion_x()
    move.target_pose.pose.position.y = punto.get_posicion_y()
    move.target_pose.pose.position.z = 0.0
    move.target_pose.pose.orientation.x = 0.0
    move.target_pose.pose.orientation.y = 0.0
    move.target_pose.pose.orientation.z = punto.get_orientacion_z()
    move.target_pose.pose.orientation.w = punto.get_orientacion_w()

    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)  # se crea el cliente de la accion
    client.wait_for_server()  # esperamos a que el servidor este activo

    client.send_goal(move)  # enviamos el goal
    rospy.loginfo("Enviado el goal...")
    client.wait_for_result()  # esperamos el resultado
    #print('Resultado: %f'%(client.get_result())) # imprime el resultado


# --- main() ---
print("Pulsa 1 para ir al Laboratorio")
print("Pulsa 2 para ir a la Habitacion 321")
print("Pulsa 3 para ir a los Banyos")
print("------------------------------------------")
numero = int(input('Elija una opcion: '))

if numero == 1:
    Punto_Lab = Punto(no= "Laboratorio", pos_x=-2.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
    mover_robot_a_punto(Punto_Lab)
    print("---------- Moviendo robot ----------")
    condicion_opciones = True

if numero == 2:
    Punto_Hab_321 = Punto(no= "Habitacion 321", pos_x=2.5, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
    mover_robot_a_punto(Punto_Hab_321)
    print("---------- Moviendo robot ----------")
    condicion_opciones = True

if numero == 3:
    Punto_Banyos = Punto(no= "Banyos", pos_x=4.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
    mover_robot_a_punto(Punto_Banyos)
    print("---------- Moviendo robot ----------")
    condicion_opciones = True
