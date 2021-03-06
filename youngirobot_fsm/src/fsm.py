#! /usr/bin/env python

import rospy
from smach import State,StateMachine
from time import sleep
import smach_ros
import actionlib
from punto import Punto
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult


class Iniciar(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])
        pose_publisher = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
        posicion_inicial = PoseWithCovarianceStamped()
        posicion_inicial.pose.pose.orientation.w = 1
        posicion_inicial.pose.pose.position.x = -1.75
        posicion_inicial.pose.pose.position.y = 1.75
        posicion_inicial.pose.pose.position.z = 0
        posicion_inicial.header.frame_id = 'map'
        pose_publisher.publish(posicion_inicial)

    def execute(self, userdata):
        sleep(1)
        if userdata.input == 1:
             return '1'
        else:
             return '0'
class Esperar(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)
        sm.userdata.sm_input = int(input('Que quieres hacer? 1(navegacionindicada)/0(navegacionautonoma): '))
        if(userdata.input == 0 or userdata.input == 1):
            if userdata.input == 1:
                return '1'
            else:
                return '0'
        else:
            return '0'
            raise ValueError("Error al introduccir el valor")
class Navegacion_indicada(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)
        # --- main() ---
        print("Pulsa 1 para ir al Laboratorio")
        print("Pulsa 2 para ir a la Habitacion 321")    
        print("Pulsa 3 para ir a los Banyos")
        print("------------------------------------------")
        numero = int(input('Elija una opcion: '))

        if numero == 1:
            Punto_Lab = Punto(no= "Laboratorio", pos_x=-2.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Lab)
            Punto_Lab_Real = Punto(no= "Laboratorio", pos_x=0.0, pos_y=0.0, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Lab_Real)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True

        if numero == 2:
            Punto_Hab_321 = Punto(no= "Habitacion 321", pos_x=2.5, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Hab_321)
            Punto_Hab_321_Real = Punto(no= "Habitacion 321", pos_x=-0.25, pos_y=1.0, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Hab_321_Real)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True

        if numero == 3:
            Punto_Banyos = Punto(no= "Banyos", pos_x=4.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Banyos)
            Punto_Banyos_Real = Punto(no= "Banyos", pos_x=-0.5, pos_y=1.75, ori_z=0.0, ori_w=1.0)
            self.mover_robot_a_punto(Punto_Banyos_Real)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True
        sm.userdata.sm_input = int(input('Que quieres hacer? 0(Esperar)/1(navegacionautonoma): '))
        if(userdata.input == 0 or userdata.input == 1):
            if userdata.input == 1:
                return '1'
            else:
                return '0'
        else:
            return '0'
            raise ValueError("Error al introduccir el valor")
    def mover_robot_a_punto(self, punto):

        #rospy.init_node('fsm')

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

class Navegacion_autonoma(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def mover_robot_a_punto(self, punto):

        #rospy.init_node('fsm')

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

    def execute(self, userdata):
        sleep(1)
        # --- main() ---
        print("Pulsa 1 para realizar la ruta manyanera")
        print("Pulsa 2 para realizar la ruta del medio dia")
        print("Pulsa 3 para realizar la ruta nocturna")
        print("------------------------------------------")
        numero = int(input('Elija una opcion: '))

        Punto_Lab = Punto(no= "Laboratorio",pos_x=-2.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
        Punto_Hab_321 = Punto(no= "Habitacion 321", pos_x=2.5, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
        Punto_Banyos = Punto(no= "Banyos", pos_x=4.0, pos_y=-4.0, ori_z=0.0, ori_w=1.0)
        
        ruta_manyanera = [Punto_Hab_321, Punto_Banyos]
        ruta_medio_dia = [Punto_Lab, Punto_Banyos]
        ruta_nocturna = [Punto_Banyos, Punto_Lab]

        Punto_Lab_Real = Punto(no= "Laboratorio", pos_x=0.0, pos_y=0.0, ori_z=0.0, ori_w=1.0)
        Punto_Hab_321_Real = Punto(no= "Habitacion 321", pos_x=-0.25, pos_y=1.0, ori_z=0.0, ori_w=1.0)
        Punto_Banyos_Real = Punto(no= "Banyos", pos_x=-0.5, pos_y=1.75, ori_z=0.0, ori_w=1.0)

        ruta_manyanera = [Punto_Hab_321_Real, Punto_Banyos_Real]
        ruta_medio_dia = [Punto_Lab_Real, Punto_Banyos_Real]
        ruta_nocturna = [Punto_Banyos_Real, Punto_Lab_Real]

        if numero == 1:
            for i in ruta_manyanera:
                self.mover_robot_a_punto(i)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True

        if numero == 2:
            for i in ruta_medio_dia:
                self.mover_robot_a_punto(i)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True

        if numero == 3:
            for i in ruta_nocturna:
                self.mover_robot_a_punto(i)
            print("---------- Moviendo robot ----------")
            condicion_opciones = True
        sm.userdata.sm_input = int(input('Que quieres hacer? 1(navegacionindicada)/0(Esperar): '))
        if(userdata.input == 0 or userdata.input == 1):
            if userdata.input == 1:
                return '1'
            else:
                return '0'
        else:
            return '0'
            raise ValueError("Error al introduccir el valor")
                    
try:
  rospy.init_node('test_fsm', anonymous=True)
  sm = StateMachine(outcomes=['success'])
  sm.userdata.sm_input = 1
  with sm:
    iniciar = int(input("Quieres iniciar el robot? 1/0:"))
    if(iniciar == 0 or iniciar == 1):
        if(iniciar == 1):
            StateMachine.add('Iniciar', Iniciar(), transitions={'1':'Esperar','0':'Iniciar'}, remapping={'input':'sm_input','output':'input'})
            StateMachine.add('Esperar', Esperar(), transitions={'1':'Navegacion_indicada','0':'Navegacion_autonoma'}, remapping={'input':'sm_input','output':'input'})
            StateMachine.add('Navegacion_indicada', Navegacion_indicada(), transitions={'0':'Esperar','1':'Navegacion_autonoma'}, remapping={'input':'sm_input','output':'input'})
            StateMachine.add('Navegacion_autonoma', Navegacion_autonoma(), transitions={'1':'Navegacion_indicada','0':'Esperar'}, remapping={'input':'sm_input','output':'input'})
        else:
            print("No se ha ejecutado el programa, vuelve a ejecutarlo")
        sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
        sis.start()
        sm.execute()
        rospy.spin()
        sis.stop()
    else:
        raise ValueError("Error al introduccir el valor")
        
except ValueError as error:
  print("Se ha producido un error " + str(error))
  rospy.spin()