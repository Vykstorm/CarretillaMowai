#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de rutinas para localizar el robot
# dentro de un tablero (con forma de malla).


from matriz import mat
from thread import start_new_thread
from threading import Condition
from time import sleep

from sensores import get_sensores, get_sensores_discretizados, get_dist_recorrida
from probs import *
from mapa import colores, nodos_centro


#########################################################
# Las siguientes matrices definen probabilidades condicionales en el centro
# del tablero.
# Tenemos varias variables observables: LI, LD, F
# LI = 1 si el sensor lateral izquierdo es alto, 0 en caso contrario
# LD = 1 si el sensor lateral derecho es alto, 0 en caso contrario
# F = 1 si ambos sensores frontales dan valores altos, 0 en caso contrario

# La siguiente matriz define las probabilidades de que LI = 1 condicionado
# con que estemos en cada una de las casillas X11,X12, ... y con la orientación
# del robot.
# P(LI = 1 | X11, N), P(LI = I | X12, N)

IL_norte = mat(3,3)
IL_norte[0] = [.9, .5, .5]
IL_norte[1] = [.5, .05, .05]
IL_norte[2] = [.9, .05, .05]

IL_sur = mat(3,3)
IL_sur[0] = [.05, .05, .9]
IL_sur[1] = [.05, .05, .9]
IL_sur[2] = [.5, .5, .9] 

IL_este = mat(3,3)
IL_este[0] = [.9, .5, .9]
IL_este[1] = [.05, .05, .9]
IL_este[2] = [.05, .05, .9]

IL_oeste = mat(3,3)
IL_oeste[0] = [.5, .05, .05]
IL_oeste[1] = [.5, .05, .05]
IL_oeste[2] = [.9, .5, .9]

IL = {'norte':IL_norte, 'sur':IL_sur, 'este':IL_este, 'oeste':IL_oeste}

DL_norte = mat(3,3)
DL_norte[0] = [.5, .5, .9]
DL_norte[1] = [.05, .05, .9]
DL_norte[2] = [.05, .05, .9]

DL_sur = mat(3,3)
DL_sur[0] = [.5, .05, .05]
DL_sur[1] = [.5, .05, .05]
DL_sur[2] = [.9, .5, .5]

DL_este = mat(3,3)
DL_este[0] = [.05, .05, .9]
DL_este[1] = [.05, .05, .9]
DL_este[2] = [.9, .5, .9]


DL_oeste = mat(3,3)
DL_oeste[0] = [.9, .5, .9]
DL_oeste[1] = [.5, .05, .05]
DL_oeste[2] = [.5, .05, .05]
 
DL = {'norte':DL_norte, 'sur':DL_sur, 'este':DL_este, 'oeste':DL_oeste}

F_norte = mat(3,3)
F_norte[0] = [.9, .05, .9]
F_norte[1] = [.05, .05, .05]
F_norte[2] = [.05, .05, .05]

F_sur = mat(3,3)
F_sur[0] = F_norte[2]
F_sur[1] = F_norte[1]
F_sur[2] = F_norte[0]

F_este = mat(3,3)
F_este[0] = [.05, .05, .9]
F_este[1] = [.05, .05, .9]
F_este[2] = [.05, .05, .9]

F_oeste = mat(3,3)
F_oeste[0] = [.9, .05, .05]
F_oeste[1] = [.05, .05, .05]
F_oeste[2] = [.9, .05, .05]

F = {'norte':F_norte, 'sur':F_sur, 'este':F_este, 'oeste':F_oeste}

#########################################################




# Estas variables booleanas activan/desactivan el uso de una variable observable del robot para
# su localización
LOCALIZATION_USE_LATERAL_SENSORS = False
LOCALIZATION_USE_FRONTAL_SENSORS = True
LOCALIZATION_USE_DISTANCE = True
LOCALIZATION_USE_COLOR = True

# Estas variables son parámetrso que indican la importancia que se le da a
# cada variable para estimar la posición del robot.
LOCALIZATION_DISTANCE_FACTOR = 1
LOCALIZATION_LATERAL_SENSORS_FACTOR = 1
LOCALIZATION_FRONTAL_SENSORS_FACTOR = 1
LOCALIZATION_COLOR_FACTOR = 1

LOCALIZATION_UPDATE_TIME = .1

# Con esta clase podremos estimar la posición del robot en el tablero.
class gps:
	# Constructor: Debe pasarse como parámetros,el nodo a priori del robot
	# dentro del tablero y su dirección de movimiento ('este', 'oeste', 'norte', 
	# 'sur').
	def __init__(self, nodo, orientacion):
		grid = mat(3,3)
		fila, col = int(nodo[1])-1,int(nodo[2])-1
		pos = [fila, col]
		if (pos[0] < 0) or (pos[0] >= grid.get_width()) or (pos[1] < 0) or (pos[1] >= grid.get_height()):
			raise IndexError()
		self.orientacion = orientacion
		self.dist = get_dist_recorrida()
		self.initial_pos = pos
			
		self.alive = True
		self.update_lock = Condition()
		self.lock = Condition()
		
		self.inicializar_probs()
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
	
	# Este método devuelve el nodo donde se estima que está el robot.
	# (Cuya casilla tenga más probabilidad).
	def get_nodo(self):
		pos = self.get_pos()
		return 'X' + str(pos[0]+1) + str(pos[1]+1)
	
	
	# Este método inicializa la matriz de probabilidades.		
	def inicializar_probs(self):
		self.actualizar_probs()
	
	# Este método es invocado cada cierto intervalo de tiempo, para estimar la posición
	# actual del robot (estima las probabilidades de estar en cada una de las casillas)
	def actualizar_probs(self):
		# Tenemos variables variables observables en nuestro modelo, que son, la distancia recorrida
		# aproximada (d), el color (c), los sensores LI, LD, F, el punto de partida X0 del robot y su 
		# orientación O = {N,S,E,W} 
		# Y una variable no observable que es la casilla del tablero donde se encuentra el robot 
		# X
		
		n, m = [3, 3]
		pos = self.initial_pos
		orientacion = self.orientacion
		
		# Obtenemos el color 
		ic, il, dc, dl, c = get_sensores_discretizados()
		c = (c >= 2)
		ic = (ic >= 1)
		dc = (dc >= 1)
		il = (il >= 1)
		dl = (dl >= 1)

		
		# Obtenemos la distancia recorrida
		d = get_dist_recorrida() - self.dist
		
		
		# Calcular las probabilidades condicionadas... P(vB | X11), P(vB | X12), ... 
		# o si el color observado es negro... P(vN | X11), P(vN | X12), ...
		
		if not c: # Color observado es blanco.
			# P(vB | X blanco) = 0.95 y P(vB | X negro) = 0.3
			cp = colores.map(lambda x,i,j:.95 if x == 0 else 0.3)
		else:	# Color observado es negro
			# P(vN | X blanco) = 0.05 y P(vN | X negro) = 0.7
			cp = colores.map(lambda x,i,j:.05 if x == 0 else 0.7)

		# Calculamos las probabilidades condicionales P(a<=d<=a+1 | X11, X0, O=N), P(a<=d<=a+1 | X12, X0, O=N), ...
		# Estas probabilidades son: probabilidad de que la distancia estimada recorrida desde el punto inicial, sabiendo
		# que hemos llegado hasta la casilla X11, X12,... está en el rango [a,a+1]
		# Puede expresarse de la siguiente forma: Si d' es una variable observable que indica la distancia real recorrida desde
		# el punto inicial X0..
		# P(a<=d<=a+1 | X11, X0) = P(a<=d<=a+1 | b<=d'<=b+1) = (1-k)^|a-b| si a != b o k si a = b
		a = int(d)
		dp = mat(n,m).map(lambda x,i,j:abs(pos[0]-i)+abs(pos[1]-j))
		dp = dp.map(lambda b,i,j:0.8 if a==b else pow(1-0.8,abs(a-b)))
	
		# Tendremos también en cuenta la orientación del robot...
		# P(a<=d<=a+1 | X11, X0, O=N/S/E/W)
		if orientacion == 'sur':
			dp = dp.map(lambda x,i,j:x if (j == pos[1]) and (i >= pos[0]) else 0.1)
		elif orientacion == 'norte':
			dp = dp.map(lambda x,i,j:x if (j == pos[1]) and (i <= pos[0]) else 0.1)
		elif orientacion == 'este':
			dp = dp.map(lambda x,i,j:x if (j >= pos[1]) and (i == pos[0]) else 0.1)
		elif orientacion == 'oeste':
			dp = dp.map(lambda x,i,j:x if (j <= pos[1]) and (i == pos[0]) else 0.1)
			
		# Calculamos las probabilidades condicionales P(LI alto | X11), P(LI alto | X12), ...
		# Si el sensor izquierdo tiene un valor alto, P(L1 no alto | X11), P(LI no alto | X12), ... en caso contrario
		ILp = IL[orientacion]
		if not il:
			ILp = ILp.map(lambda x,i,j:1-x)
			
		# Hacemos lo mismo para el sensor lateral derecho y los frontales...
		DLp = DL[orientacion]
		if not dl:
			DLp = DLp.map(lambda x,i,j:1-x)
		
		Fp = F[orientacion]
		if (not ic) or (not dc):
			Fp = Fp.map(lambda x,i,j:1-x) 


                # Modificar las probabilidades condicionadas en base a la importancia que se le da
                # a cada variable con la que estimamos cada posición.
                k = LOCALIZATION_DISTANCE_FACTOR
                dp = dp.map(lambda x,i,j:x*k +abs(.5 - x)*(1-k))
                k = LOCALIZATION_LATERAL_SENSORS_FACTOR
                ILp = ILp.map(lambda x,i,j:x*k +abs(.5 - x)*(1-k))
                k = LOCALIZATION_LATERAL_SENSORS_FACTOR
                DLp = DLp.map(lambda x,i,j:x*k +abs(.5 - x)*(1-k))
                k = LOCALIZATION_FRONTAL_SENSORS_FACTOR
                Fp = Fp.map(lambda x,i,j:x*k +abs(.5 - x)*(1-k))
                k = LOCALIZATION_COLOR_FACTOR
                cp = cp.map(lambda x,i,j:x*k +abs(.5 - x)*(1-k))

		
		# Tenemos varias probabilidades condicionales.. P(V1 | X11), P(V2 | X11), ...  
		# Donde V1, V2, .. son nuestras variables observables
		# Nos interesa calcular P(X11 | V1 ^ V2 ^ .. ^ Vn). 
		# Podemos calcular P(V1 ^ V2 ^ ... ^ VN | X11) = P(V1 | X11) * P(V2 | X11) * ...
		# Porque las variables observables las consideramos independientes entre sí.
                V = []
                if LOCALIZATION_USE_DISTANCE:
                        V.append(dp)
                if LOCALIZATION_USE_COLOR:
                        V.append(cp)
                if LOCALIZATION_USE_FRONTAL_SENSORS:
                        V.append(Fp)
                if LOCALIZATION_USE_LATERAL_SENSORS:
                        V.append(ILp)
                        V.append(DLp)


		
		pInv = map(lambda *args:reduce(lambda x,y:x*y, args), *V)
		
		# Probabilidades a priori de las casillas..
		# P(X11), P(X12), ...
		# No tenemos información a priori
		pPriori = [1.0/(n*m)] * (n*m)
		
		# Calculamos P(X11 | V1^V2^...^Vn), P(X12 | V1^V2^...^Vn), ...
		self.probs = mat(3,3)
		self.probs.from_list(bayes(pInv, pPriori))

	def run(self):
		self.lock.acquire()
		while self.alive:
			with self.update_lock:
				self.actualizar_probs() 
			self.lock.wait(LOCALIZATION_UPDATE_TIME)
	
	def __str__(self):
		return self.get_nodo().__str__()
		
	def __repr__(self):
		return self.get_nodo().__repr__()
	
	# Destructor: Se invoca cuando ya no es necesario estimar la posición del robot.
	# (libera recursos) 
	def close(self):
		with self.lock:
			self.alive = False
			self.lock.notify()





# Código de depuración
if __name__ == '__main___':
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
