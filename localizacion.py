#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de rutinas para localizar el robot
# dentro de un tablero (con forma de malla).


from matriz import mat
from thread import start_new_thread
from threading import Condition
from time import sleep
from sensores import get_sensores_discretizados, get_dist_recorrida
from probs import *



# Esta clase representará una posición del robot dentro del tablero
class posicion:
	# Constructor
	def __init__(self, i,j):
		self.i = i
		self.j = j
	
	# Devuelve la fila donde se encuentra el robot
	def fila(self):
		return self.i
	
	# Devuelve la columna donde se encuentra el robot
	def columna(self):
		return self.j

# Con esta clase podremos estimar la posición del robot en el tablero.
class gps:
	# Constructor: Debe pasarse como parámetros, la posición a priori del robot
	# dentro del tablero y su dirección de movimiento ('este', 'oeste', 'norte', 
	# 'sur')
	def __init__(self, pos, orientacion):
		grid = mat(3,3)
		if (pos.fila() < 0) or (pos.fila() >= grid.width()) or (pos.columna() < 0) or (pos.columna() >= grid.height()):
			raise IndexError()
		self.pos = pos
		self.orientacion = orientacion
	
	# Este método devuelve la posición estimada actual del robot.
	def get_posicion(self):
		return self.posicion
	
	
	# Destructor: Se invoca cuando ya no es necesario estimar la posición del robot.
	# (libera recursos) 
	def __del__(self):
		pass
	
