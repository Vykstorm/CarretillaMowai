#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# La clase ruta representa una ruta que debe seguir el robot.
# SerÃ¡ una secuencia de movimientos que debe realizar el robot hasta 
# llegar al final de la misma.

from collections import deque
from sets import Set
from mapa import *

# Esta clase representa un estado del robot.
# ESTADO = NODO + ORIENTACIÓN

class estado:
	def __init__(self, nodo, orientacion):
		if (not nodo in nodos) or (not orientacion in cardinales):
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
		
		
	def __eq__(self, otro):
		return (self.nodo == otro.nodo) and (self.orientacion == otro.orientacion)
		
	def __hash__(self):
		return hash(self.nodo + self.orientacion)
		
E = estado

# Esta clase representa una ruta que debe seguir un robot para desplazarse
# de un nodo a otro.
class ruta:
	# Constructor. Se le indica los estados del robot por los que debe pasar
	# para recorrer el camino marcado por la ruta.
	def __init__(self, estados):
		self.estados = estados
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
				if not movimientos[orientacion].is_connected(A,B):
					raise Exception()
				return [movimientos[orientacion].get(A,B)]
#				return [movimientos['este'].get(A,B)]
		else: # Hay un estado o ninguno.
			return []
		
	
	# Este método hace que el estado inicial sea aquel que le antecede y además
	# consume el siguiente movimiento de la ruta. Devuelve false si ya se había llegado
	# el destino, true en caso contrario
	def avanzar(self):
		if len(self.movimientos) == 0:
			return False
		self.movimientos.popleft()
		self.estados.popleft()
		return True
		
	# Este método devuelve el primer estado de la ruta.
	def estado_actual(self):
		return self.estados[0]
		
	# Este método devuelve el estado final de la ruta.
	def estado_final(self):
		return self.estados[-1]
	
	# Este método devuelve el estado que antecede al estado inicial o actual.
	def siguiente_estado(self):
		if len(self.movimientos) == 0:
			raise Exception()
		return self.estados[1]
		
	# Este método devuelve el siguiente movimiento para alcanzar el siguiente estado
	# a partir del estado actual.
	def siguiente_movimiento(self):
		if len(self.movimientos) == 0:
			raise Exception()
		return self.movimientos[0]

	def __str__(self):
		return str(self.estados)

	def __repr__(self):
		if len(self.movimientos) == 0:
			return ''
		return reduce(lambda x,y:x+' -> '+repr(y), self.estados[1:], repr(self.estados[0]))



# Esta clase representa un planificador de rutas. Esta clase crea una ruta
# de coste mínimo entre dos nodos cualesquiera del mapa.

class planificador_ruta:
	# Constructor: Toma como parámetro dos nodos AyB y la orientación inicial en el nodo de 
	# inicio A
	# Es decir, el estado inicial es el par (A, orientación).
	# El conjunto de estados finales son: (B, *), es decir, cualquier estado con el nodo B
	# pero cualquier orientación.
	def __init__(self, A, B, orientacion):
		self.estados = self.calcular_ruta(A,B,orientacion)
		
	# Esta rutina debe devolver la ruta de coste mínimo entre A y B
	def calcular_ruta(self, A, B):
		pass
		
	# Esta función devuelve la ruta calculada previamente
	def get_ruta(self):
		return ruta(self.estados)
		



# Esta clase representa el algoritmo A* para el calculo de la ruta de coste 
# mínimo entre dos nodos.
class planificador_Aestrella(planificador_ruta):
	def __init__(self, *args):
		planificador_ruta.__init__(self, *args)
		
	# Implementación del A*
	def calcular_ruta(self, A, B, orientacion): 
		return Aestrella(A,B,orientacion)
		
		
		
		
# Métodos auxiliares para el Algoritmo A*
# Heuristica de coste de un estado X, sabiendo que el nodo destino es A 
def H(X,A): 
	return dist_manhattan(X.get_nodo(), A)
	 
# Devuelve los estados vecinos de X
def V(X):
	return map(lambda B:E(B,orientaciones.get(X.get_nodo(),B)) mapa.get_neighbours(X.get_nodo()))
#	return map(lambda B:E(B,'este'), mapa.get_neighbours(X.get_nodo()))

# Comprueba si Y es vecino de X.
def isV(X,Y):
	return mapa.is_connected(X.get_nodo(),Y.get_nodo()) and (Y.get_orientacion() == orientaciones.get(X.get_nodo(),Y.get_nodo()))
#	return mapa.is_connected(X.get_nodo(),Y.get_nodo())

# Coste de ir de un estado X a un estado Y
def C(X,Y):
	return costes[X.get_orientacion()].get(X.get_nodo(),Y.get_nodo())
#	return costes['este'].get(X.get_nodo(),Y.get_nodo())
	
# Comprueba si el estado X es un estado final, sabiendo que el nodo A es el
# nodo destino
def F(X,A):
	return X.get_nodo() == A

# Implementación del algoritmo Aestrella
def Aestrella(A,B,orientacion):
	# Inicializamos la lista de abiertos y cerrados.
	abiertos = Set()
	cerrados = Set()
	fAbiertos = dict() # Contiene las evaluaciones de coste+heurística de los estados en abiertos.
	fCerrados = dict() # Igual pero para los estados cerrados
	
	# Creamos el nodo inicial
	inicio = E(A,orientacion) 
	
	# Añadimos el nodo inicial a abiertos
	abiertos.add(inicio)
	fAbiertos[inicio] = 0
	
	# Mientras abiertos no este vacío.
	while len(abiertos) > 0:
		# Obtener nodo en abiertos con menor coste+heurística.
		m = min(fAbiertos.values())
		N = filter(lambda x:x[1] == m, fAbiertos.iteritems())[0][0]

		# Si N es estado final, hemos acabado...
		if F(N,B):
			cerrados.add(N)
			break
		
		# Eliminamos N de abiertos y lo añadimos a cerrados.
		abiertos.remove(N)
		cerrados.add(N)
		fCerrados[N] = fAbiertos[N]
		del fAbiertos[N]
		
		# Obtenemos los sucesores de N
		sucesores = V(N)
		
		# Por cada sucesor...
		for S in sucesores:
			# Calcular coste+heurística del sucesor
			fs = C(N,S) + H(S,B)
			
			# Si el sucesor ya está en abiertos o en cerrados, y es un nodo mejor, 
			# añadirlo a abiertos y eliminar apariciones del mismo en abiertos y cerrados.
			# Si no es mejor, descartarlo.
			if ((S in abiertos) and (fAbiertos[S] <= fs)) or ((S in cerrados) and (fCerrados[S] <= fs)):
				continue
			
			# Eliminar apariciones del sucesor en abiertos y en cerrados
			if (S in abiertos):
				abiertos.remove(S)
				del fAbiertos[S]
			if (S in cerrados):
				cerrados.remove(S)
				del fCerrados[S]
			
			# Añadir el sucesor a abiertos
			abiertos.add(S)
			fAbiertos[S] = fs
	
	# Hemos tenido éxito en la búsqueda?
	if len(filter(lambda X:F(N,B),cerrados)) == 0:
		raise Exception() # Búsqueda no exitosa
		
		
	# Reorganizamos los estados.
	ruta = []
	actual = inicio
	ruta.append(actual)
	cerrados.remove(actual)
	while len(cerrados) > 0:
		actual = filter(lambda X:isV(actual,X), cerrados)
		if len(actual)==0:
			raise Exception()
		actual = actual[0]
		ruta.append(actual)
		cerrados.remove(actual)

	return ruta
	
