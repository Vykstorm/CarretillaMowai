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

# Nodos del mapa
nodos = ['A', 'B', 'C', 'N1', 'N2', 'N3', 'N4', 'N5','X11', 'X12', 'X13', 'X21', 'X22', 'X23', 'X31', 'X32', 'X33']


# El siguiente gráfo puede usarse para conocer la vecindad de cada nodo.

mapa = grafo(nodos)
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



# Los siguientes gráfos definen para cada orientación posible del robot
# (este, oeste, norte, sur), el movimiento necesario para ir de un nodo a 
# cada uno de sus vecinos.
# destino.

# Posibles movimientos del robot 
acciones = ['left', 'right', 'forward', 'backward'] 

	#			N4			
	###########		#############
	#	X11		X12		X13		#
	#							#
#N2		X21		X22		X23		#
	#							#
	#	X31		X32		X33		#
	###########		#############
	#			N1				#



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

# Orientación NORTE
m_norte = grafo(nodos)

# Orientación SUR
m_sur = grafo(nodos)


abrv = {'L':'left', 'R':'right', 'B':'backward', 'F':'forward'}
movimientos = dict(zip(['este', 'oeste', 'norte', 'sur'], map(lambda m:m.map(lambda v,i,j:None if (v==None) or (not v in abrv) else abrv[v]), [m_este, m_oeste, m_norte, m_sur])))



###################################################################
# Los siguientes gráfos definen para cada orientación posible del robot
# (este, oeste, norte, sur), la orientación final del robot al llegar a un
# nodo, partiendo de otro nodo vecino.

# Posibles orientaciones del robot.
cardinales = ['este', 'oeste', 'norte', 'sur']

# Orientación ESTE
o_este = grafo(nodos)
o_este.connect('A', ['N1', 'N5'], ['E', 'N'])
o_este.connect('B', 'N2', 'N')
o_este.connect('C', 'N5', 'S')
o_este.connect('N1', ['A', 'N3', 'X32'], ['S', 'N', 'N'])
o_este.connect('N2', ['B', 'N4', 'X21'], ['S', 'E', 'E'])
o_este.connect('N3', ['N4', 'N1', 'N5'], ['O', 'O', 'E'])
o_este.connect('N4', ['N2', 'N3', 'X12'], ['S', 'S', 'S'])
o_este.connect('N5', ['N3', 'C', 'A'], ['O', 'N', 'O'])
o_este.connect('X11', ['X12', 'X21'], ['E', 'S'])
o_este.connect('X12', ['X11', 'X22', 'X13', 'N4'], ['O', 'S', 'E', 'N'])
o_este.connect('X13', ['X12', 'X23'], ['O', 'S'])
o_este.connect('X21', ['X11', 'X31', 'X22', 'N2'], ['N', 'S', 'E', 'O'])
o_este.connect('X22', ['X21', 'X12', 'X23', 'X32'], ['O', 'N', 'E', 'S'])
o_este.connect('X23', ['X13', 'X22', 'X33'], ['N', 'O', 'S'])
o_este.connect('X31', ['X21', 'X32'], ['N', 'E'])
o_este.connect('X32', ['X31', 'X22', 'X33', 'N1'], ['O', 'N', 'E', 'S'])
o_este.connect('X33', ['X32', 'X23'])

# Orientación OESTE
o_oeste = grafo(nodos)

# Orientación NORTE
o_norte = grafo(nodos)

# Orientación SUR
o_sur = grafo(nodos)


abrv = {'E':'este', 'O':'oeste', 'sur':'S', 'N':'norte'}
orientaciones = dict(zip(['este', 'oeste', 'norte', 'sur'], map(lambda m:m.map(lambda v,i,j:None if (v==None) or (not v in abrv) else abrv[v]), [o_este, o_oeste, o_norte, o_sur])))




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

# Orientación NORTE
c_norte = grafo(nodos)

# Orientación SUR
c_sur = grafo(nodos)

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
	for k,o in costes.iteritems():
		try:
			if len([(A,B) for A in nodos for B in nodos if mapa.is_fully_connected(A,B) and not o.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if not mapa.is_fully_connected(A,B) and o.is_fully_connected(A,B)]) > 0:
				raise Exception()
			if len([(A,B) for A in nodos for B in nodos if o.is_fully_connected(A,B) and ((not type(o.get(A,B)) in [str]) or (not c.get(A,B) in cardinales))]) > 0:
				raise Exception()
		except:
			raise Exception("Matriz de costes " + k + " no valida")
