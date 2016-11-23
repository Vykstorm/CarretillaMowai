#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n: Este script almacena toda la informaciÃ³n sobre la estructura
# del almacÃ©n.


# Estructura del almacén

####
	
##########################
#		 N4			# C	 #
#	####	####	#	 #
#	#		   # 	#	 #
#	#		   #	#	 #
# N2		   # N3	 N5	 #
#			   #		 #
#	#		   #	#	 #
#	#		   #	#	 #
# B	#		   #	#	 #
########	####	#	 #
#		 N1			#	 #
#	#################	 #
# A						 #
##########################


####
# Zonas clave del mapa: Puntos A,B,C
# El resto de puntos, serán nodos intermedios que podrÃ¡ usar el algoritmo
# de planificación de ruta para calcular la ruta de coste mÃ­nimo.
# Los nodos se numeran de abajo hacia arriba y de izquierda a derecha
# (exceptuando los nodos en el centro del tablero).


# El centro del tablero será una malla de 3x3 casillas. Cada casilla es un nodo
# adicional. ...

	#			N4			
	###########		#############
	#	X11		X12		X13		#
	#							#
#N2		X21		X22		X23		#
	#							#
	#	X31		X32		X33		#
	###########		#############
	#			N1				#

# Las casillas del centro del tablero tendrán un color asignado (para facilitar
# la localización del robot en esa zona): Serán casillas negras o blancas


	#			N4			
	###########		#############
	#	B		N		B		#
	#							#
#N2		N		B		N		#
	#							#
	#	B		N		B		#
	###########		#############
	#			N1				#


from matriz import mat
from grafo import grafo





###################################################################
class f_mat(mat):
	def __init__(self, n, m, format_func):
		mat.__init__(self, n, m)
		self.format_func = format_func
	def __repr__(self):
		s = ''
		for i in range(0,self.get_width()):
			s = s + '|'
			for j in range(0,self.get_height()):
				s = s + self.format_func(i,j,self.get(i,j))
			s = s + ' |\n'
		return s
	

# Esta matriz indica que colores tienen las casillas del centro del tablero.
# 0 si es blanco y 1 si es negro

colores = f_mat(3,3,lambda i,j,v: ('blanco' if v == 0 else 'negro').center(10))
colores[0] = [0, 1, 0]
colores[1] = [1, 0, 1]
colores[2] = [0, 1, 0]





###################################################################
# Las siguientes matrices almacenan los costes de ir de un nodo a otro nodo (son usadas
# por el algoritmo de planificación de ruta de coste mínimo).
# Habrá cuatro matrices. Cada una de ellas almacenará el coste de ir de un nodo a otro en 
# función de su orientación (este, oeste,norte,sur)

# El coste se mide en unidades: El coste de ir de un nodo a otro es la distancia manhattan
# entre ambos (midiendo la distancia en términos de casillas y no en cm)

# Nodos del centro del tablero
nodos_centro = ['X11', 'X12', 'X13', 'X21', 'X22', 'X23', 'X31', 'X32', 'X33']

# Nodos del mapa
nodos = ['A', 'B', 'C', 'N1', 'N2', 'N3', 'N4', 'N5'] + nodos_centro


####
# EL siguiente gráfo almacena donde están los obstáculos, sea G(V,A) el gráfo.
# Si el par <X,Y> de nodos está en A, es decir, forman una arista, querrá decir
# que entre X e Y hay un obstáculo, por lo que el robot no puede desplazarse 
# de X->Y o de Y->X 
class grafo_obstaculos(grafo):
	def __init__(self, *args):
		grafo.__init__(self, *args)
	
	def block(self, A, B):
		grafo.connect(self, A,B)
		grafo.connect(self, B,A)
		
	def unblock(self, A,B):
		grafo.disconnect(self, A,B)
		grafo.disconnect(self, B,A)
		
	def is_blocked(self, A,B):
		return grafo.is_fully_connected(self, A,B)

obstaculos = grafo_obstaculos(nodos)


# El siguiente gráfo puede usarse para conocer la vecindad de cada nodo.

class grafo_mapa(grafo):
	def __init__(self, *args):
		grafo.__init__(self, *args)
		
	def get(self, A, B):
		return grafo.get(self, A, B) if not obstaculos.is_blocked(A,B) else None


mapa = grafo_mapa(nodos)
mapa.connect('A', ['N1', 'N5'])
mapa.connect('B', 'N2')
mapa.connect('C', 'N5')
mapa.connect('N1', ['A', 'N3', 'X32'])
mapa.connect('N2', ['B', 'N4', 'X21'])
mapa.connect('N3', ['N4', 'N1', 'N5'])
mapa.connect('N4', ['N2', 'N3', 'X12'])
mapa.connect('N5', ['N3', 'C', 'A'])
mapa.connect('X11', ['X12', 'X21'])
mapa.connect('X12', ['X11', 'X22', 'X13', 'N4'])
mapa.connect('X13', ['X12', 'X23'])
mapa.connect('X21', ['X11', 'X31', 'X22', 'N2'])
mapa.connect('X22', ['X21', 'X12', 'X23', 'X32'])
mapa.connect('X23', ['X13', 'X22', 'X33'])
mapa.connect('X31', ['X21', 'X32'])
mapa.connect('X32', ['X31', 'X22', 'X33', 'N1'])
mapa.connect('X33', ['X32', 'X23'])


###################################################################
# Los siguientes gráfos definen para cada orientación posible del robot
# (este, oeste, norte, sur), el movimiento necesario para ir de un nodo a 
# cada uno de sus vecinos.
# destino.

# Posibles movimientos del robot 
acciones = ['left', 'right', 'forward', 'backward'] 

# Orientación ESTE
m_este = grafo(nodos)
m_este.connect('A', ['N1', 'N5'], ['L', 'F'])
m_este.connect('B', 'N2', 'L')
m_este.connect('C', 'N5', 'R')
m_este.connect('N1', ['A', 'N3', 'X32'], ['B', 'F', 'L'])
m_este.connect('N2', ['B', 'N4', 'X21'], ['R', 'L', 'F'])
m_este.connect('N3', ['N4', 'N1', 'N5'], ['L', 'R', 'F'])
m_este.connect('N4', ['N2', 'N3', 'X12'], ['B', 'F', 'R'])
m_este.connect('N5', ['N3', 'C', 'A'], ['B', 'L', 'R'])
m_este.connect('X11', ['X12', 'X21'], ['F', 'R'])
m_este.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['B', 'R', 'F', 'L'])
m_este.connect('X13', ['X12', 'X23'], ['B', 'R'])
m_este.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['L', 'R', 'F', 'B'])
m_este.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['B', 'L', 'F', 'R'])
m_este.connect('X23', ['X13', 'X22', 'X33'], ['L', 'B', 'R'])
m_este.connect('X31', ['X21', 'X32'], ['L', 'F'])
m_este.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['B', 'L', 'F', 'R'])
m_este.connect('X33', ['X32', 'X23'], ['B', 'L'])


# Orientación OESTE
m_oeste = grafo(nodos)
m_oeste.connect('A', ['N1', 'N5'], ['R', 'B'])
m_oeste.connect('B', 'N2', 'R')
m_oeste.connect('C', 'N5', 'L')
m_oeste.connect('N1', ['A', 'N3', 'X32'], ['F', 'B', 'R'])
m_oeste.connect('N2', ['B', 'N4', 'X21'], ['L', 'R', 'B'])
m_oeste.connect('N3', ['N4', 'N1', 'N5'], ['R', 'L', 'B'])
m_oeste.connect('N4', ['N2', 'N3', 'X12'], ['F', 'B', 'L'])
m_oeste.connect('N5', ['N3', 'C', 'A'], ['F', 'R', 'L'])
m_oeste.connect('X11', ['X12', 'X21'], ['B', 'L'])
m_oeste.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['F', 'L', 'B', 'R'])
m_oeste.connect('X13', ['X12', 'X23'], ['F', 'L'])
m_oeste.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['R', 'L', 'B', 'F'])
m_oeste.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['F', 'R', 'B', 'L'])
m_oeste.connect('X23', ['X13', 'X22', 'X33'], ['R', 'F', 'L'])
m_oeste.connect('X31', ['X21', 'X32'], ['R', 'B'])
m_oeste.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['F', 'R', 'B', 'L'])
m_oeste.connect('X33', ['X32', 'X23'], ['F', 'R'])

# Orientación NORTE
m_norte = grafo(nodos)
m_norte.connect('A', ['N1', 'N5'], ['F','R'])
m_norte.connect('B', 'N2', 'F')
m_norte.connect('C', 'N5', 'B')
m_norte.connect('N1', ['A', 'N3', 'X32'], ['L', 'R', 'F'])
m_norte.connect('N2', ['B', 'N4', 'X21'], ['B', 'F', 'R'])
m_norte.connect('N3', ['N4', 'N1', 'N5'], ['F', 'B', 'R'])
m_norte.connect('N4', ['N2', 'N3', 'X12'], ['L', 'R', 'B'])
m_norte.connect('N5', ['N3', 'C', 'A'], ['L', 'F', 'B'])
m_norte.connect('X11', ['X12', 'X21'], ['R', 'B'])
m_norte.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['L', 'B', 'R', 'F'])
m_norte.connect('X13', ['X12', 'X23'], ['L', 'B'])
m_norte.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['F', 'B', 'R', 'L'])
m_norte.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['L', 'F', 'R', 'B'])
m_norte.connect('X23', ['X13', 'X22', 'X33'], ['F', 'L', 'B'])
m_norte.connect('X31', ['X21', 'X32'], ['F', 'R'])
m_norte.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['L', 'F', 'R', 'B'])
m_norte.connect('X33', ['X32', 'X23'], ['L', 'F'])

# Orientación SUR
m_sur = grafo(nodos)
m_sur.connect('A', ['N1', 'N5'], ['B', 'L'])
m_sur.connect('B', 'N2', 'B')
m_sur.connect('C', 'N5', 'F')
m_sur.connect('N1', ['A', 'N3', 'X32'], ['R', 'L', 'B'])
m_sur.connect('N2', ['B', 'N4', 'X21'], ['F', 'B', 'L'])
m_sur.connect('N3', ['N4', 'N1', 'N5'], ['B', 'F', 'L'])
m_sur.connect('N4', ['N2', 'N3', 'X12'], ['R', 'L', 'F'])
m_sur.connect('N5', ['N3', 'C', 'A'], ['R', 'B', 'F'])
m_sur.connect('X11', ['X12', 'X21'], ['L', 'F'])
m_sur.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['R', 'F', 'L', 'B'])
m_sur.connect('X13', ['X12', 'X23'], ['R', 'F'])
m_sur.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['B', 'F', 'L', 'R'])
m_sur.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['R', 'B', 'L', 'F'])
m_sur.connect('X23', ['X13', 'X22', 'X33'], ['B', 'R', 'F'])
m_sur.connect('X31', ['X21', 'X32'], ['B', 'L'])
m_sur.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['R', 'B', 'L', 'F'])
m_sur.connect('X33', ['X32', 'X23'], ['R', 'B'])

abrv = {'L':'left', 'R':'right', 'B':'backward', 'F':'forward'}
movimientos = dict(zip(['este', 'oeste', 'norte', 'sur'], map(lambda m:m.map(lambda v,i,j:None if (v==None) or (not v in abrv) else abrv[v]), [m_este, m_oeste, m_norte, m_sur])))



###################################################################
# Los siguientes gráfos definen la orientación final del robot al llegar a un
# nodo, partiendo de otro nodo vecino.

# Posibles orientaciones del robot.
cardinales = ['este', 'oeste', 'norte', 'sur']

orientaciones = grafo(nodos)
orientaciones.connect('A', ['N1', 'N5'], ['E', 'N'])
orientaciones.connect('B', 'N2', 'N')
orientaciones.connect('C', 'N5', 'S')
orientaciones.connect('N1', ['A', 'N3', 'X32'], ['S', 'N', 'N'])
orientaciones.connect('N2', ['B', 'N4', 'X21'], ['S', 'E', 'E'])
orientaciones.connect('N3', ['N4', 'N1', 'N5'], ['O', 'O', 'E'])
orientaciones.connect('N4', ['N2', 'N3', 'X12'], ['S', 'S', 'S'])
orientaciones.connect('N5', ['N3', 'C', 'A'], ['O', 'N', 'O'])
orientaciones.connect('X11', ['X12', 'X21'], ['E', 'S'])
orientaciones.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['O', 'S', 'E', 'N'])
orientaciones.connect('X13', ['X12', 'X23'], ['O', 'S'])
orientaciones.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['N', 'S', 'E', 'O'])
orientaciones.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['O', 'N', 'E', 'S'])
orientaciones.connect('X23', ['X13', 'X22', 'X33'], ['N', 'O', 'S'])
orientaciones.connect('X31', ['X21', 'X32'], ['N', 'E'])
orientaciones.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['O', 'N', 'E', 'S'])
orientaciones.connect('X33', ['X32', 'X23'])


abrv = {'E':'este', 'O':'oeste', 'sur':'S', 'N':'norte'}
orientaciones = orientaciones.map(lambda v,i,j:None if (v==None) or (not v in abrv) else abrv[v])




###################################################################
# Los siguientes gráfos definen para cada orientación posible del robot 
# (este, oeste, norte, sur), el coste del movimiento necesario para ir de
# un nodo a otro.

# Posición (x,y) de los nodos del mapa (usando A como punto de origen, el este como eje X y el norte como eje Y)
casillas = {'A':[0,0], 'B':[0,2], 'C':[5,5], 'N1':[2,1], 'N4':[2,5], 'N2':[0,3], 'N3':[4,3], 'N5':[5,3]}
casillas.update([('X'+str(i+1)+str(j+1),[2+j,4-i]) for i in range(0,3) for j in range(0,3)])

# Penalizaciones en los giros..
COSTE_GIRO_ESQUINA = 3 # Coste de doblar una esquina.
COSTE_GIRO_NODO = 2 # Coste de girar 90º en un nodo

# Este es un método auxiliar que nos ayudará a crear las matrices de costes (calcula la distancia manhattan entre
# dos nodos)
def manhattan(p0, p1):
	if type(p0) == str:
		return manhattan(casillas[p0],p1)
	if type(p1) == str:
		return manhattan(p0, casillas[p1])
	return sum(map(lambda v0,v1:abs(v1-v0), p0, p1))
dist_manhattan = manhattan

# Orientación ESTE
cge, cgn,d = COSTE_GIRO_ESQUINA, COSTE_GIRO_NODO, manhattan
c_este = grafo(nodos)
c_este.connect('A', ['N1', 'N5'], [cgn+cge+d('A','N1'), d('A','N5')+cge])
c_este.connect('B', 'N2', cgn+d('B','N2'))
c_este.connect('C', 'N5', cgn+d('C','N5'))
c_este.connect('N1', ['A', 'N3', 'X32'], [2*cgn+d('N1', 'A'), d('N1', 'N3')+cge, cgn+1])
c_este.connect('N2', ['B', 'N4', 'X21'], [cgn+d('N2','B'), cgn+d('N2','N4')+cge, 1])
c_este.connect('N3', ['N4', 'N1', 'N5'], [cgn+d('N3', 'N4')+cge, cgn+d('N3','N1')+cge, 1])
c_este.connect('N4', ['N2', 'N3', 'X12'], [2*cgn+d('N4', 'N2')+cge, d('N4','N3')+cge, cgn+1])
c_este.connect('N5', ['N3', 'C', 'A'], [2*cgn+1, cgn+d('N5','C'), cgn+d('N5','A')+cge])
c_este.connect('X11', ['X12', 'X21'], [1, cgn+1])
c_este.connect('X12', ['X11', 'X22', 'X13', 'N4'], [2*cgn+1, cgn+1, 1, cgn+1])
c_este.connect('X13', ['X12', 'X23'], [2*cgn, cgn+1])
c_este.connect('X21', ['X11', 'X31', 'X22', 'N2'], [cgn+1,cgn+1,1,2*cgn+1])
c_este.connect('X22', ['X21', 'X12', 'X23', 'X32'], [2*cgn+1, cgn+1, 1, cgn+1])
c_este.connect('X23', ['X13', 'X22', 'X33'], [cgn+1, 2*cgn+1, cgn+1])
c_este.connect('X31', ['X21', 'X32'], [cgn+1, 1])
c_este.connect('X32', ['X31', 'X22', 'X33', 'N1'], [2*cgn+1,cgn+1,1,cgn+1])
c_este.connect('X33', ['X32', 'X23'], [2*cgn+1,cgn+1])

# Orientación OESTE
c_oeste = grafo(nodos)
c_oeste.connect('A', ['N1', 'N5'], [cgn+cge+d('A','N1'), 2*cgn+cge+d('A', 'N5')])
c_oeste.connect('B', 'N2', cgn+d('B','N2'))
c_oeste.connect('C', 'N5', cgn+d('C', 'N5'))
c_oeste.connect('N1', ['A', 'N3', 'X32'], [cge+d('N1','A'), 2*cgn+cge+d('N1','N3'), cgn+1])
c_oeste.connect('N2', ['B', 'N4', 'X21'], [cgn+d('N2','B'), cgn+cge+d('N2','N4'), 2*cgn+1])
c_oeste.connect('N3', ['N4', 'N1', 'N5'], [cgn+cge+d('N3','N4'), cgn+cge+d('N3','N1'), 2*cgn+1])
c_oeste.connect('N4', ['N2', 'N3', 'X12'], [cge+d('N4','N2'), 2*cgn+cge+d('N4', 'N3'), cgn+1])
c_oeste.connect('N5', ['N3', 'C', 'A'], [1, cgn+d('N5','C'), cgn+cge+d('N5', 'A')])
c_oeste.connect('X11', ['X12', 'X21'], [2*cgn+1, cgn+1])
c_oeste.connect('X12', ['X11', 'X22', 'X13', 'N4'], [1, cgn+1, 2*cgn+1, cgn+1])
c_oeste.connect('X13', ['X12', 'X23'], [1, cgn+1])
c_oeste.connect('X21', ['X11', 'X31', 'X22', 'N2'], [cgn+1, cgn+1, 2*cgn+1, 1])
c_oeste.connect('X22', ['X21', 'X12', 'X23', 'X32'], [1, cgn+1, 2*cgn+1, cgn+1])
c_oeste.connect('X23', ['X13', 'X22', 'X33'], [cgn+1, 1, cgn+1])
c_oeste.connect('X31', ['X21', 'X32'], [cgn+1, 2*cgn+1])
c_oeste.connect('X32', ['X31', 'X22', 'X33', 'N1'], [1, cgn+1, 2*cgn+1, cgn+1])
c_oeste.connect('X33', ['X32', 'X23'], [1, cgn+1])

# Orientación NORTE
c_norte = grafo(nodos)
c_norte.connect('A', ['N1', 'N5'], [cge+d('A','N1'), cgn+cge+d('A','N5')])
c_norte.connect('B', 'N2', d('B','N2'))
c_norte.connect('C', 'N5', 2*cgn+d('C','N5'))
c_norte.connect('N1', ['A', 'N3', 'X32'], [cgn+cge+d('N1','A'), cgn+cge+d('N1','N3'), 1])
c_norte.connect('N2', ['B', 'N4', 'X21'], [2*cgn+d('N2','B'), cge+d('N2','N4'), cgn+1])
c_norte.connect('N3', ['N4', 'N1', 'N5'], [cge+d('N3','N4'), 2*cgn+cge+d('N3','N1'), cgn+1])
c_norte.connect('N4', ['N2', 'N3', 'X12'], [cgn+cge+d('N4','N2'), cgn+cge+d('N4','N3'), 2*cgn+1])
c_norte.connect('N5', ['N3', 'C', 'A'], [cgn+1, d('N5','C'), 2*cgn+cge+d('N5','A')])
c_norte.connect('X11', ['X12', 'X21'], [cgn+1, 2*cgn+1])
c_norte.connect('X12', ['X11', 'X22', 'X13', 'N4'], [cgn+1, 2*cgn+1, cgn+1, 1])
c_norte.connect('X13', ['X12', 'X23'], [cgn+1, 2*cgn+1])
c_norte.connect('X21', ['X11', 'X31', 'X22', 'N2'], [1, 2*cgn+1, cgn+1, cgn+1])
c_norte.connect('X22', ['X21', 'X12', 'X23', 'X32'], [cgn+1, 1, cgn+1, 2*cgn+1])
c_norte.connect('X23', ['X13', 'X22', 'X33'], [1, cgn+1, 2*cgn+1])
c_norte.connect('X31', ['X21', 'X32'], [1, cgn+1])
c_norte.connect('X32', ['X31', 'X22', 'X33', 'N1'], [cgn+1, 1, cgn+1, 2*cgn+1])
c_norte.connect('X33', ['X32', 'X23'], [cgn+1, 1])

# Orientación SUR
c_sur = grafo(nodos)
c_sur.connect('A', ['N1', 'N5'], [2*cgn+cge+d('A','N1'), cgn+cge+d('A','N5')])
c_sur.connect('B', 'N2', 2*cgn+d('B','N2'))
c_sur.connect('C', 'N5', d('C','N5'))
c_sur.connect('N1', ['A', 'N3', 'X32'], [cgn+cge+d('N1','A'), cgn+cge+d('N1','N3'), 2*cgn+d('N1','X32')])
c_sur.connect('N2', ['B', 'N4', 'X21'], [d('N2','B'), 2*cgn+cge+d('N2','N4'), cgn+d('N2','X21')])
c_sur.connect('N3', ['N4', 'N1', 'N5'], [2*cgn+cge+d('N3','N4'), cge+d('N3','N1'), cgn+d('N3','N5')])
c_sur.connect('N4', ['N2', 'N3', 'X12'], [cgn+cge+d('N4','N2'), cgn+cge+d('N4','N3'), d('N4','X12')])
c_sur.connect('N5', ['N3', 'C', 'A'], [cgn+d('N5','N3'), 2*cgn+d('N5','C'), cge+d('N5','A')])
c_sur.connect('X11', ['X12', 'X21'], [cgn+1, 1])
c_sur.connect('X12', ['X11', 'X22', 'X13', 'N4'], [cgn+1, 1, cgn+1, 2*cgn+d('X12','N4')])
c_sur.connect('X13', ['X12', 'X23'], [cgn+1, 1])
c_sur.connect('X21', ['X11', 'X31', 'X22', 'N2'], [2*cgn+1, 1, cgn+1, cgn+d('N2','X21')])
c_sur.connect('X22', ['X21', 'X12', 'X23', 'X32'], [cgn+1, 2*cgn+1, cgn+1, 1])
c_sur.connect('X23', ['X13', 'X22', 'X33'], [2*cgn+1, cgn+1, 1])
c_sur.connect('X31', ['X21', 'X32'], [2*cgn+1, cgn+1])
c_sur.connect('X32', ['X31', 'X22', 'X33', 'N1'], [cgn+1, 2*cgn+1, cgn+1, 1])
c_sur.connect('X33', ['X32', 'X23'], [cgn+1, 2*cgn+1])

costes = {'este':c_este, 'oeste':c_oeste, 'norte':c_norte, 'sur':c_sur}


###################################################################
# Código de depuración para verificar las matrices anteriores.
if __name__ == '__main__':
	# Verificamos las matrices de movimientos
	for k,m in movimientos.iteritems():
		try:
			if len([(A,B) for A in nodos for B in nodos if mapa.is_fully_connected(A,B) and not m.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if not mapa.is_fully_connected(A,B) and m.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if m.is_fully_connected(A,B) and (not m.get(A,B) in acciones)]) > 0:
				raise Exception()
		except:
			raise Exception("Matriz de movimientos " + k + " no valida") 
	# Verificamos las matrices de costes.
	for k,c in costes.iteritems():
		try:
			if len([(A,B) for A in nodos for B in nodos if mapa.is_fully_connected(A,B) and not c.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if not mapa.is_fully_connected(A,B) and c.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if c.is_fully_connected(A,B) and ((not type(c.get(A,B)) in [float, int]) or (c.get(A,B) < 0))]) > 0:
				raise Exception()
		except:
			raise Exception("Matriz de costes " + k + " no valida")
	# Verificamos las matrices de orientaciones
