#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# MÃ³dulo que define una serie de rutinas que establecen los patrones
# de movimiento del robot.


from thread import start_new_thread
from threading import Condition
from moway_lib import *
from time import sleep


# Configuración de los motores.
ROBOT_FORWARD_SPEED = 15 # Velocidad de movimiento del robot
ROBOT_ROTATION_SPEED = 5 # Velocidad de giro estático del robot 
ROBOT_ROTATION_AXIS = CENTER # Eje de giro del robot (CENTER o WHEEL)
ROBOT_ROTATION_MAX_ANGLE = 5 # Angulo máximo de giro.
ROBOT_ROTATION_DELAY = .2;


# Esta clase representa una acción o una secuencia de movimientos del robot.
# Solo puede haber una secuencia de movimientos activa al mismo tiempo
class accion:
	def __init__(self, lock):
		self.lock = lock
	
	# Esta función se ejecuta múltiples veces mientras la acción siga activa.
	# Debe finalizar su ejecución si el hilo invocador recibe una notificación.
	def ejecutar(self):
		pass
	
class forward(accion):
	def __init__(self, lock):
		accion.__init__(self, lock)
	
	def ejecutar(self):
		# Ejecutamos los comandos para movernos hacia delante.
		moway.command_moway(CMD_GO,0)
		self.lock.wait()
		moway.command_moway(CMD_STOP,0)
	
class giro_izq(accion):
	def __init__(self, lock):
		accion.__init__(self, lock)
		
	def ejecutar(self):
		# Ejecutamos los comandos para movernos hacia la izquierda.
		moway.set_rotation(ROBOT_ROTATION_MAX_ANGLE)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_ROTATELEFT,0)
		self.lock.wait(ROBOT_ROTATION_DELAY)
		moway.command_moway(CMD_STOP,0)s
class giro_der(accion):
	def __init__(self, lock):
		accion.__init__(self, lock)
	
	def ejecutar(self):
		# Ejecutamos los comandos para movernos hacia la derecha.
		moway.set_rotation(ROBOT_ROTATION_MAX_ANGLE)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_ROTATERIGHT,0)
		self.lock.wait(ROBOT_ROTATION_DELAY)
		moway.command_moway(CMD_STOP,0)

class parado(accion):
	def __init__(self, lock):
		accion.__init__(self, lock)
	
	def ejecutar(self): 
		self.lock.wait()

lock = Condition()

# Esta variable indica la acción actual del robot.
accion_actual = parado(lock)

# Esta función auxiliar ejecuta los comandos correspondientes en base a cual 
# sea la acción actual, de forma asíncrona.
def ejecutar_acciones():
	while True:
		with lock:
			accion_actual.ejecutar()

start_new_thread(ejecutar_acciones, ())

# Este método hará que el robot comienze a girar en una de las direcciones.
def girar(sentido):
	global accion_actual
	with lock:
		if (sentido == 'left') and not isinstance(accion_actual, giro_izq):
			accion_actual = giro_izq(lock)
			lock.notify()
		elif (sentido == 'right') and not isinstance(accion_actual, giro_der):
			accion_actual = giro_der(lock)
			lock.notify()
	
# Este método hara que el robot comienza a moverse hacia delante.
def move():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, forward):
			accion_actual = forward(lock)
			lock.notify()

# Este método mantendrá al robot parado.
def stop():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, parado):
			accion_actual = parado(lock)
			lock.notify()
	


