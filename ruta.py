#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# La clase ruta representa una ruta que debe seguir el robot.
# SerÃ¡ una secuencia de movimientos que debe realizar el robot hasta 
# llegar al final de la misma.

from collections import deque
from mapa import movimientos, mapa, nodos, orientaciones

# Esta clase representa un estado del robot.
# ESTADO = NODO + ORIENTACIÓN
class estado:
	def __init__(self, nodo, orientacion):
		if (not nodo in nodos) or (not orientacion in orientaciones):
			raise Exception()
		self.nodo = nodo
		self.orientacion = orientacion
	
	def get_nodo(self):
		return self.nodo 
	
	def get_orientacion(self):
		return self.orientacion
		
	def __str__(self):
		return '(' + self.get_nodo() + ', ' + self.get_orientacion() + ')'
		
	def __repr__(self):
		return repr(self.__str__())


# Esta clase representa una ruta que debe seguir un robot para desplazarse
# de un nodo a otro.
class ruta:
	# Constructor. Se le indica los estados del robot por los que debe pasar
	# para recorrer el camino marcado por la ruta.
	def __init__(self, estados):
		self.movimientos = deque(self.calcular_movimientos(estados))
	
	# Este método calcula el conjunto de movimientos secuenciales que debe
	# realizar el robot en base a los estados por los que debe pasar.
	def calcular_movimientos(self, estados):
		if len(estados) > 1:
			if len(estados) > 2:
				return self.calcular_movimientos(estados[:-1]) + self.calcular_movimientos(estados[-2:])
			else:
				A = estados[0].get_nodo()
				B = estados[1].get_nodo()
				orientacion = estados[0].get_orientacion()
				print A,B
				if not movimientos[orientacion].is_connected(A,B):
					raise Exception()
				return [movimientos[orientacion].get(A,B)]
		else: # Hay un estado o ninguno.
			return []
		
	
	# Este método deberá devolver el siguiente movimiento a realizar.
	def siguiente_movimiento(self):
		if len(self.movimientos) == 0:
			return False
		movimiento = self.movimientos[0]
		self.movimientos.popleft()
		return movimiento





# Esta clase representa un planificador de rutas. Esta clase crea una ruta
# de coste mínimo entre dos nodos cualesquiera del mapa.

class planificador_ruta:
	# Constructor: Toma como parámetro dos nodos AyB 
	def __init__(self, A, B):
		if (not A in nodos or not B in nodos):
			raise Exception()
		self.estados = self.calcular_ruta(A,B)
		
	# Esta rutina debe devolver la ruta de coste mínimo entre A y B
	def calcular_ruta(self, A, B):
		pass
		
	# Esta función devuelve la ruta calculada previamente
	def get_ruta(self):
		return ruta(self.estados)
		



# Esta clase representa el algoritmo A* para el calculo de la ruta de coste 
# mínimo entre dos nodos.
class planificador_Aestrella(planificador_ruta):
	def __init__(self, A, B):
		planificador_ruta.__init__(self, A, B)
		
	# Implementación del A*
	def calcular_ruta(self, A, B): 
		# TODO
		pass
