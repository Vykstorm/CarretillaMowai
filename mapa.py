#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script almacena toda la información sobre la estructura
# del almacén.


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
# El resto de puntos, serán nodos intermedios que podrá usar el algoritmo
# de planificación de ruta para calcular la ruta de coste mínimo.
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
# la localización del robot en esa zona): Será casillas negras o blancas


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


# Las siguientes matrices almacenan los costes de ir de un nodo a otro nodo (son usadas
# por el algoritmo de planificación de ruta de coste mínimo).
# Habrá cuatro matrices. Cada una de ellas almacenará el coste de ir de un nodo a otro en 
# función de su orientación (este, oeste,norte,sur)

# El coste se mide en unidades: El coste de ir de un nodo a otro es la distancia manhattan
# entre ambos (midiendo la distancia en términos de casillas y no en cm)

# Los giros para tomar una esquina en los pasillos, tendrán una penalización...
coste_giro_esquina = 3
# Los giros de 90º en las intersecciones y en el centro del tablero tendrán otra...
coste_giro_nodos = 2

# Nodos del mapa
nodos = ['A', 'B', 'C', 'N1', 'N2', 'N3', 'N4', 'N5','X11', 'X12', 'X13', 'X21', 'X22', 'X23', 'X31', 'X32', 'X33']
# Casillas de los nodos del mapa (usando A como punto de origen, el este como eje X y el norte como eje Y)
casillas = {'A':[0,0], 'B':[0,2], 'C':[5,5], 'N1':[2,1], 'N4':[2,5], 'N2':[0,3], 'N3':[4,3], 'N5':[5,3]}
casillas.update([('X'+str(i+1)+str(j+1),[2+j,4-i]) for i in range(0,3) for j in range(0,3)])


# Este es un método auxiliar que nos ayudará a crear la matriz de costes (calcula la distancia manhattan entre
# dos nodos)
def manhattan(p0, p1):
	if type(p0) == str:
		return manhattan(casillas[p0],p1)
	if type(p1) == str:
		return manhattan(p0, casillas[p1])
	return sum(map(lambda v0,v1:abs(v1-v0), p0, p1))


# Dirección Este.

##########################
#		 N4 ->		# C  #
#	####	####	#	 #			#			N4->	
#	#		   # 	#	 #			###########		#############
#	#		   #	#	 #			#	X11->	X12->	X13->	#
# N2 ->		   #N3-> N5->#			#							#
#			   #		 #		#N2	->	X21->	X22->	X23->	#
#	#		   #	#	 #			#							#
#	#		   #	#	 #			#	X31->	X32->	X33->	#
# B	#		   #	#	 #			###########		#############
########	####	#	 #			#			N1->			#
#		 N1	->		#	 #
#	#################	 #
# A	->					 #
##########################

d = manhattan
ge = coste_giro_esquina
gn = coste_giro_nodos

c_este = grafo(nodos)
c_este.connect('A', ['N1', 'N5'], [gn + ge + d('A','N1'),  ge + d('A', 'N5')])
c_este.connect('B', 'N2',  gn + d('B','N2'))
c_este.connect('C', 'N5', gn + d('C','N5'))
c_este.connect('N1', ['N3', 'X32', 'A'], [ge + d('N1', 'N3'), gn + d('N1', 'X32'), 2*gn + d('N1', 'A') + ge])
c_este.connect('N2', ['B', 'X21', 'N4'], [gn + d('N2','B'), d('N2', 'X21'), gn + d('N2', 'N4') + ge])
c_este.connect('N3', ['N1', 'N4', 'N5'], [gn + d('N3', 'N1') + ge, gn + d('N3','N4') + ge, d('N3', 'N5')])
c_este.connect('N4', ['N2', 'N3', 'X12'], [2*gn + d('N4', 'N2') + ge, d('N4', 'N3') + ge, gn + d('N4','X12')]) 
c_este.connect('N5', ['C', 'N3', 'A'], [gn + d('N5','C'), 2*gn + d('N5','N3'), gn + d('N5', 'A') + ge])

c_este.connect('X11', ['X12', 'X21'], [1, gn + 1])
c_este.connect('X12', ['X11', 'X22', 'X13', 'N4'], [2*gn + 1, gn + 1, 1, gn + 1])
c_este.connect('X13', ['X12', 'X23'], [2*gn + 1, gn + 1])
c_este.connect('X21', ['X11', 'X22', 'X31', 'N2'], [gn + 1, 1, gn +1, 2*gn + 1])
c_este.connect('X22', ['X12', 'X23', 'X32', 'X21'], [gn+1, 1,gn+1,2*gn+1])
c_este.connect('X23', ['X13', 'X22', 'X33'], [gn+1,2*gn+1,gn+1])
c_este.connect('X31', ['X21', 'X32'], [gn+1,1])
c_este.connect('X32', ['X31', 'X22', 'X33', 'N1'], [2*gn+1,gn+1,1,gn+1])
c_este.connect('X33', ['X32', 'X23'], [2*gn+1, gn+1])



# Dirección Oeste.

##########################
#	 	<- N4 		#<-C #
#	####	####	#	 #			#			N4	
#	#		   # 	#	 #			###########		#############
#	#		   #	#	 #			# <-X11	  <-X12	 	<-X13	#
#<-N2		   #<-N3 <-N5#			#							#
#			   #		 #		#N2	  <-X21	  <-X22		<-X23	#
#	#		   #	#	 #			#							#
#	#		   #	#	 #			# <-X31	  <-X32		<-X33	#
# B	#		   #	#	 #			###########		#############
########	####	#	 #			#			N1				#
#		<-N1		#	 #
#	#################	 #
#<-A					 #
##########################

c_oeste = grafo(nodos)


# Dirección Norte.

##########################
#		 N4 ->		# C  #
#	####	####	#	 #			#			N4->	
#	#		   # 	#	 #			###########		#############
#	#		   #	#	 #			#	X11->	X12->	X13->	#
# N2 ->		   #N3-> N5->#			#							#
#			   #		 #		#N2	->	X21->	X22->	X23->	#
#	#		   #	#	 #			#							#
#	#		   #	#	 #			#	X31->	X32->	X33->	#
# B	#		   #	#	 #			###########		#############
########	####	#	 #			#			N1->			#
#		 N1	->		#	 #
#	#################	 #
# A	->					 #
##########################

c_norte = grafo(nodos)

# Dirección Sur.

##########################
#		 N4 ->		# C  #
#	####	####	#	 #			#			N4->	
#	#		   # 	#	 #			###########		#############
#	#		   #	#	 #			#	X11->	X12->	X13->	#
# N2 ->		   #N3-> N5->#			#							#
#			   #		 #		#N2	->	X21->	X22->	X23->	#
#	#		   #	#	 #			#							#
#	#		   #	#	 #			#	X31->	X32->	X33->	#
# B	#		   #	#	 #			###########		#############
########	####	#	 #			#			N1->			#
#		 N1	->		#	 #
#	#################	 #
# A	->					 #
##########################

c_sur = grafo(nodos)
