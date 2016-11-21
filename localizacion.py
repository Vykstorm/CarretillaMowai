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
from mapa import colores



POSITION_UPDATE_TIME = 1

# Con esta clase podremos estimar la posición del robot en el tablero.
class gps:
	# Constructor: Debe pasarse como parámetros, la posición a priori del robot
	# dentro del tablero y su dirección de movimiento ('este', 'oeste', 'norte', 
	# 'sur')
	def __init__(self, pos, orientacion):
		grid = mat(3,3)
		if (pos[0] < 0) or (pos[0] >= grid.get_width()) or (pos[1] < 0) or (pos[1] >= grid.get_height()):
			raise IndexError()
		self.orientacion = orientacion
		self.dist = get_dist_recorrida()
		self.initial_pos = pos
			
		self.inicializar_probs()
		self.alive = True
		self.update_lock = Condition()
		self.lock = Condition()
		start_new_thread(self.run, ())

	# Este método devuelve una matriz de probabilidades.
	# El valor en la posición (i,j) de la matriz es la probabilidad de que 
	# el robot este en la casilla (i,j) del tablero.
	def get_probs(self):
		with self.update_lock:
			p = self.probs
		return p
	
	
	# Este método devuelve la posición estimada actual del robot.
	# Será aquella la casilla que tenga asignada mayor probabilidad
	def get_pos(self):
		probs = self.get_probs()
		p = probs.to_list()
		i = p.index(max(p))
		return [i / probs.get_height(), i % probs.get_height()]
	
	
	
	# Este método inicializa la matriz de probabilidades.		
	def inicializar_probs(self):
		self.probs = mat(3,3)
		self.probs[self.initial_pos[0],self.initial_pos[1]] = 1
	
	# Este método es invocado cada cierto intervalo de tiempo, para estimar la posición
	# actual del robot (estima las probabilidades de estar en cada una de las casillas)
	def actualizar_probs(self):
		# Tenemos dos variables no observables en nuestro modelo, que son, la distancia recorrida
		# aproximada (d) y el color (c)
		# Y una variable no observable que es la distancia real recorrida (d') desde que se inicio el 
		# último movimiento
		
		n, m = self.probs.get_size()
		pos = self.initial_pos
		orientacion = self.orientacion
		
		# Obtenemos el color 
		ic, il, dc, dl, c = get_sensores_discretizados()
		c = (c >= 2)
		
		# Obtenemos la distancia recorrida
		d = get_dist_recorrida() - self.dist

		# Calcular las probabilidades condicionadas... P(vB | X11), P(vB | X12), ... 
		# o si el color observado es negro... P(vN | X11), P(vN | X12), ...
		
		if not c: # Color observado es blanco.
			# P(vB | X blanco) = 0.95 y P(vB | X negro) = 0.3
			cp = colores.map(lambda x,i,j:0.95 if x == 0 else 0.3)
		else:	# Color observado es negro
			# P(vN | X blanco) = 0.05 y P(vN | X negro) = 0.7
			cp = colores.map(lambda x,i,j:0.05 if x == 0 else 0.7)

		# Calculamos las probabilidades condicionadas... P(X11 | vB), V(X12 | vB), ...
		# o P(X11 | vN), P(X12 | vN), ...
		# Usando el teorema de bayes sin información a priori.
		cpPost = mat(n,m)
		cpPost.from_list(bayes(cp.to_list(), [1] * (n*m)))
		
		# Calculamos las probabilidades condicionales P(a<=d<=a+1 | X11), P(a<=d<=a+1 | X12), ...
		# Estas probabilidades son: probabilidad de que la distancia estimada esté entre dos
		# valores condicionado con que estoy en la casilla X, o lo que es lo mismo ->
		# P(a<=d<=a+1 | X) = P(a<=d<=a+1 | b<=d'<=b+1) con a y b enteros.
		# P(a<=d<=a+1 | b<=d'<=b+1) = (1-k)^|a-b| si a != b o k si a = b
		a = int(d)
		dp = mat(n,m).map(lambda x,i,j:abs(pos[0]-i)+abs(pos[1]-j))
		dp = dp.map(lambda b,i,j:0.8 if a==b else pow(1-0.8,abs(a-b)))
		self.probs = dp

		# Calculamos las probabilidades a priori... P(X11), P(X12), ...
		# En base a la orientación y a la posición inicial del robot. Si el movimiento es
		# por ejemplo de norte a sur y la posición inicial es (x,y)
		# Las probabilidades a priori de las casillas (x,y), (x,y+1), ... serán 1, el resto 
		# serán 0.
		if orientacion == 'sur':
			dpPriori = mat(n,m).map(lambda x,i,j:1 if (j == pos[1]) and (i >= pos[0]) else 0)
		elif orientacion == 'norte':
			dpPriori = mat(n,m).map(lambda x,i,j:1 if (j == pos[1]) and (i <= pos[0]) else 0)
		elif orientacion == 'este':
			dpPriori = mat(n,m).map(lambda x,i,j:1 if (j >= pos[1]) and (i == pos[0]) else 0)
		elif orientacion == 'oeste':
			dpPriori = mat(n,m).map(lambda x,i,j:1 if (j <= pos[1]) and (i == pos[0]) else 0)
			
		# Calculamos las probs a posteriori... P(X11 | a<=d<=a+1), P(X12 | a<=d<=a+1), ...
		dpPost = mat(n,m)
		dpPost.from_list(bayes(dp.to_list(), dpPriori.to_list()))
			
		
		# Finalmente calculamos P(X11 | a<=d<=a+1, vB)
		# Como las variables observables son independientes, podemos calcular estas probabilidades
		# como un producto de probabilidades condicionales:
		# P(X11 | a<=d<=a+1, vB) = P(X11 | a<=d<=a+1) * P(X11 | vB) 
		self.probs.from_list(map(lambda *args:reduce(lambda x,y:x*y, args, 1), cpPost.to_list(), dpPost.to_list()))
			
		# Normalizamos las probabilidades
		s = sum(self.probs.to_list())
		self.probs = self.probs.map(lambda x,i,j:x/s)
	def run(self):
		self.lock.acquire()
		while self.alive:
			with self.update_lock:
				self.actualizar_probs() 
			self.lock.wait(POSITION_UPDATE_TIME)
	
	def __str__(self):
		return self.get_pos().__str__()
		
	def __repr__(self):
		return self.get_pos().__repr__()
	
	# Destructor: Se invoca cuando ya no es necesario estimar la posición del robot.
	# (libera recursos) 
	def close(self):
		with self.lock:
			self.alive = False
			self.lock.notify()





# Código de depuración
if __name__ == '__main__':
	import curses
	std = curses.initscr()
	
	try:
		g = gps([1,0], 'este')
		while True:
			std.clear()
			std.addstr(01, 0, repr(g.get_probs()) + '\n\n' + repr(g.get_pos()))
			std.refresh()
			sleep(.3)
	finally:
		g.close()
		curses.endwin()
