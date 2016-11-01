#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Módulo que define una serie de rutinas que establecen los patrones
# de movimiento del robot.


from thread import start_new_thread
from threading import Condition
from moway_lib import *
from time import sleep


# Configuraci�n de los motores.
ROBOT_FORWARD_SPEED = 15 # Velocidad de movimiento del robot
ROBOT_ROTATION_SPEED = 5 # Velocidad de giro est�tico del robot 
ROBOT_ROTATION_AXIS = CENTER # Eje de giro del robot (CENTER o WHEEL)
ROBOT_ROTATION_MAX_ANGLE = 5 # Angulo m�ximo de giro.
ROBOT_ROTATION_DELAY = .2;

# El siguiente método indica como debe ir cambiando de dirección el 
# robot a medida que se mueve hacia delante. Debe ser un valor en el intervalo
# [-1 y 1], 
# 0 indica que debe moverse hacia delante sin tener velocidad angular (sin giro)
# -1 Indica que debe moverse lo máximo posible hacia la izquierda mientras se mueve
# 1 Indica que debe moverse lo máximo posible hacia la derecha mientras se mueve.
# Se aceptan valores intermedios en dicho intervalo
def cambiar_direccion(cantidad):
	global direccion
	direccion = cantidad
	with motores_lock: 
		if movimiento_actual == 'forward':
			cambiar_movimiento()
	
	
# Este método basicamente establece que el robot deba moverse hacia delante.
def move():
	global movimiento_actual
	global ultimo_movimiento
	with motores_lock:
                ultimo_movimiento = movimiento_actual
		movimiento_actual = "forward"
		cambiar_movimiento()
	
# Este método establece que el robot debe pararse y luego girarse en torno a su eje central bien a la derecha o a la izquierda,
# según se indique en el parámetro ("left" or "right")
def girar(sentido):
	global movimiento_actual
	global ultimo_movimiento
	with motores_lock:
                ultimo_movimiento = movimiento_actual
		movimiento_actual = 'rotate_' + sentido
		cambiar_movimiento()


# Esté método es invocado cuando el movimiento del robot debe cambiar. Esta rutina será la encargada de 
# llamar a los comandos moway pertinentes para establecer la forma en la que debe ejecutarse la nueva secuencia de movimientos.
def cambiar_movimiento():
	#print 'Cambiando movimiento: ' + movimiento_actual
        if movimiento_actual == 'forward':
                
                moway.set_speed(ROBOT_FORWARD_SPEED)
                if direccion == 0:
                        moway.command_moway(CMD_GO,0)
                elif direccion < 0:
                        moway.set_radius(int(round(abs(direccion)*100.0)))
                        moway.command_moway(CMD_GOLEFT,0)
                elif direccion > 0:
                        moway.set_radius(int(round(abs(direccion)*100.0)))
                        moway.command_moway(CMD_GORIGHT,0)
        elif movimiento_actual == 'rotate_left':
                pass
        elif movimiento_actual == 'rotate_right':
                pass

        if ultimo_movimiento != movimiento_actual:
                motores_lock.notify()


def girar_izq():
        motores_lock.acquire()
        while movimiento_actual == 'rotate_left':
                moway.command_moway(CMD_STOP,0)
                moway.set_rotation(ROBOT_ROTATION_MAX_ANGLE)
                moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
                moway.set_speed(ROBOT_ROTATION_SPEED)
                moway.command_moway(CMD_ROTATELEFT,0)
                motores_lock.wait(ROBOT_ROTATION_DELAY)
                motores_lock.release()
                #sleep(.1)
                motores_lock.acquire()
        motores_lock.release()

def girar_der():
        motores_lock.acquire()
        while movimiento_actual == 'rotate_right':
                moway.command_moway(CMD_STOP,0)
                moway.set_rotation(ROBOT_ROTATION_MAX_ANGLE)
                moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
                moway.set_speed(ROBOT_ROTATION_SPEED)
                moway.command_moway(CMD_ROTATERIGHT,0)
                motores_lock.wait(ROBOT_ROTATION_DELAY)
                motores_lock.release()
                #sleep(.1)
                motores_lock.acquire()
        motores_lock.release()

def _girar():
        while True:
                girar_izq()
                girar_der()
        
start_new_thread(_girar, ())

                
direccion = 0;
movimiento_actual = "forward"; # Puede ser "forward", "rotate-left", "rotate-right"
ultimo_movimiento = "";
motores_lock = Condition()
