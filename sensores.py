#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripci�n:
# M�dulo que define una serie de rutinas que llevan acabo las siguientes tareas:
# - Tratamiento de la incertidumbre en los datos de los sensores de infrarrojos.
# - Conversi�n de unidades de los sensores de infrarrojos a medidas de distancia (cm)

# M�dulos importados
from collections import deque
import moway_input
from thread import start_new_thread, allocate_lock
from time import sleep
	
MAX_LENGTH_SENSOR_REG = 5
SENSOR_UPDATE_TIME = .01

# Cada objeto de esta clase recoge las mediciones de un sensor espec�fico del
# robot.
class sensor:
	# Constructor
	def __init__(self):
		self.valores = deque(maxlen=MAX_LENGTH_SENSOR_REG)
		self.update_value()
	# Este m�todo devuelve el valor actual del sensor sin procesar.
	def next_raw_value(self):
		pass
		
	# Este m�todo almacena el valor actual del sensor en el historial de 
	# mediciones.
	def update_value(self):
		self.valores.appendleft(self.next_raw_value())
	
	# Este m�todo devuelve una agregaci�n de las ultimas mediciones del sensor
	# almacenadas
	def get_value(self):
		return agregar(self.valores)
	
	# Este m�todo debe devolver el valor del sensor actual (procesado), discretizado.
	def get_categoric_value(self):
		pass
		
# La instancia de esta clase representar� el sensor izquierdo central del
# robot
class sensor_izq_central(sensor):
	def __init__(self):
		sensor.__init__(self)
		
	def next_raw_value(self):
		return moway_input.sensor_izq_central()
	
	def get_categoric_value(self):
		return discretizar(self.get_value(), .12, .52)

# La instancia de esta clase representar� el sensor izquierdo lateral del
# robot
class sensor_izq_lateral(sensor):
	def __init__(self):
		sensor.__init__(self)
		
	def next_raw_value(self):
		return moway_input.sensor_izq_lateral()
		
	def get_categoric_value(self):
		return discretizar(self.get_value(), .12, .72)

# La instancia de esta clase representar� el sensor derecho central del
# robot
class sensor_der_central(sensor):
	def __init__(self):
		sensor.__init__(self)
		
	def next_raw_value(self):
		return moway_input.sensor_der_central()
	
	def get_categoric_value(self):
		return discretizar(self.get_value(), .12, .52)

# La instancia de esta clase representar� el sensor derecho lateral del
# robot
class sensor_der_lateral(sensor):
	def __init__(self):
		sensor.__init__(self)
		
	def next_raw_value(self):
		return moway_input.sensor_der_lateral()
		
	def get_categoric_value(self):
		return discretizar(self.get_value(), .12, .72)

# La instancia de esta clase representar� el sensor del suelo del
# robot
class sensor_color(sensor):
	def __init__(self):
		sensor.__init__(self)
		
	def next_raw_value(self):
		return moway_input.sensor_color()

	def get_categoric_value(self):
		return discretizar(self.get_value(), .1, .5)
		
# Funciones auxiliares

# Esta funci�n agrega una lista de valores (sirve para agregar un conjunto 
# consecutivo de mediciones de un sensor espec�fico)
def agregar(valores):
	return sum(valores) / len(valores) # Media aritm�tica

# Este m�todo discretiza valores continuos y los convierte en valores categ�ricos,
# Puede tomar multiples par�metros:
# x, y1, y2, ..., yn
# Donde x es el valor a discretizar e y1, y2, ..., yn son umbrales, de forma que el
# valor devuelto ser�:
# 0 si x <= y1
# 1 si x <= y2
# ...
# n-1 si x <= yn
# n si x > yn
# con y1 < y2 < .. < yn
def discretizar(x, y1, *y):
	if x <= y1:
		return 0
	elif len(y) == 0:
		return 1
	else:
		return 1 + discretizar(x, y[0], *y[1:])


sensores = dict()
sensores_lock = allocate_lock()
sensores['izq_central'] = sensor_izq_central()
sensores['izq_lateral'] = sensor_izq_lateral()
sensores['der_central'] = sensor_der_central()
sensores['der_lateral'] = sensor_der_lateral()
sensores['color'] = sensor_color()

# La siguiente funci�n actualiza los sensores cada cierto intervalo
# de tiempo
def update_sensores():
	while True:
		with sensores_lock:
			# Actualizamos cada uno de los sensores
			for sensor in sensores.values():
				sensor.update_value()
		sleep(SENSOR_UPDATE_TIME)
			
start_new_thread(update_sensores, ())



# Este m�todo devuelve en forma de tupla, los valores actuales del
# sensor (procesados)
def get_sensores():
	with sensores_lock:
		indices = ['izq_central', 'izq_lateral', 'der_central', 'der_lateral', 'color']
		valores = map(lambda indice:sensores.get(indice).get_value(), indices)
	return valores
	

# Este m�todo devuelve en forma de tupla, los valores actuales del 
# sensor (procesados) pero discretizados en valores categ�ricos.
def get_sensores_discretizados():
	with sensores_lock:
		indices = ['izq_central', 'izq_lateral', 'der_central', 'der_lateral', 'color']
		valores = map(lambda indice:sensores.get(indice).get_categoric_value(), indices)
	return valores
