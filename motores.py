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
ROBOT_FORWARD_SPEED = 5 # Velocidad de movimiento del robot
ROBOT_ROTATION_SPEED = 5 # Velocidad de giro est�tico del robot 
ROBOT_ROTATION_AXIS = CENTER # Eje de giro del robot (CENTER o WHEEL)
ROBOT_ROTATION_MAX_ANGLE = 4 # Angulo m�ximo de giro.
ROBOT_ROTATION_DELAY = .2;


# Esta clase representa una acci�n o una secuencia de movimientos del robot.
# Solo puede haber una secuencia de movimientos activa al mismo tiempo
class accion:
	def __init__(self, lock):
		self.lock = lock
	
	# Esta funci�n se ejecuta m�ltiples veces mientras la acci�n siga activa.
	# Debe finalizar su ejecuci�n si el hilo invocador recibe una notificaci�n.
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
		moway.command_moway(CMD_STOP,0)
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

class vuelta_atras(accion):
        def __init__(self, lock):
                accion.__init__(self, lock)
        def ejecutar(self):
		# Ejecutamos los comandos para movernos hacia atr�s
		moway.set_rotation(180)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_ROTATERIGHT,0)
		#self.lock.wait()
                moway.wait_mot_end(0)
		moway.command_moway(CMD_STOP,0)


class girar90_izq(accion):
        def __init__(self, lock):
                accion.__init__(self, lock)
        def ejecutar(self):
		# Ejecutamos los comandos para girar 90� a la izq
		sleep(.5)
		moway.set_rotation(90)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_ROTATELEFT,0)
		#self.lock.wait()
                moway.wait_mot_end(0)
		moway.command_moway(CMD_STOP,0)
		
class girar90_der(accion):
        def __init__(self, lock):
                accion.__init__(self, lock)
        def ejecutar(self):
		# Ejecutamos los comandos para girar 90� a la der
		sleep(.5)
		moway.set_rotation(90)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_ROTATERIGHT,0)
		#self.lock.wait()
                moway.wait_mot_end(0)
		moway.command_moway(CMD_STOP,0)

class _girar180(accion):
        def __init__(self, lock):
                accion.__init__(self, lock)
        def ejecutar(self):
		# Ejecutamos los comandos para girar 180�
		#moway.set_rotation(180)
		moway.set_rotation_axis(ROBOT_ROTATION_AXIS)
		moway.set_speed(ROBOT_ROTATION_SPEED)
		moway.command_moway(CMD_TURN_AROUND,0)
		#self.lock.wait()
                moway.wait_mot_end(0)
		moway.command_moway(CMD_STOP,0)

lock = Condition()

# Esta variable indica la acci�n actual del robot.
accion_actual = parado(lock)

# Esta funci�n auxiliar ejecuta los comandos correspondientes en base a cual 
# sea la acci�n actual, de forma as�ncrona.
def ejecutar_acciones():
	while True:
		with lock:
			accion_actual.ejecutar()

start_new_thread(ejecutar_acciones, ())

# Este m�todo har� que el robot comienze a girar en una de las direcciones.
def girar(sentido):
	global accion_actual
	with lock:
		if (sentido == 'left') and not isinstance(accion_actual, giro_izq):
			accion_actual = giro_izq(lock)
			lock.notify()
		elif (sentido == 'right') and not isinstance(accion_actual, giro_der):
			accion_actual = giro_der(lock)
			lock.notify()

# Este m�todo har� que el robot gire 90� sobre la direcci�n indicada.
def girar90(sentido):
	global accion_actual
	with lock:
		if (sentido == 'left') and not isinstance(accion_actual, girar90_izq):
			accion_actual = girar90_izq(lock)
			accion_actual.ejecutar()
		elif (sentido == 'right') and not isinstance(accion_actual, girar90_der):
                        accion_actual = girar90_der(lock)
                        accion_actual.ejecutar()
                        
# Este m�todo har� que el robot gire 180�.
def girar180():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, _girar180):
			accion_actual = _girar180(lock)
			accion_actual.ejecutar() 
        

                        
# Este m�todo hara que el robot comienza a moverse hacia delante.
def move():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, forward):
			accion_actual = forward(lock)
			lock.notify()

# Este m�todo mantendr� al robot parado.
def stop():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, parado):
			accion_actual = parado(lock)
			lock.notify()
	

# Este m�todo da la vuelta al robot (cuando est� atascado en un pasillo)
def volver_atras():
	global accion_actual
	with lock:
		if not isinstance(accion_actual, vuelta_atras):
			accion_actual = vuelta_atras(lock)
			accion_actual.ejecutar()

