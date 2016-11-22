#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Este script define una representación de un gráfo dirigido.

from matriz import mat

class grafo(mat):
	# Constructor: Toma como parámetro una lista de nombres con los que
	# se podrán referenciar a los nodos.
	def __init__(self, nodos):
		mat.__init__(self, len(nodos), len(nodos), init_value=None)
		self.nodos = nodos
		self.indexes = dict(map(lambda k,i:(k,i), nodos, range(0, len(nodos))))
		
	def index_of(self,A):
		if not A in self.indexes:
			raise IndexError()
		return self.indexes[A]
		
	# Devuelve una lista con los nombres de los nodos.
	def get_nodes(self):
		return self.nodos
		
	# Conecta los nodos A y B. (A en dirección a B, con coste x).
	# B puede ser una lista de nodos. En dicho caso, Se conecta A a cada uno
	# de los indicados. A -> B1, A -> B2, ..., con costes X1, X2, ...
	# Si no se especifica el coste, se asigna coste 1 a las conexiones.
	def connect(self,A,B,*args):
		if len(args) == 0:
			if type(B) == list:
				X = [1] * len(B)
			else:
				X = 1
		else: 
			X = args[0]
		
		if ((type(B) != int) and (type(B) != list) and (type(B) != str)):
			raise Exception()
		if (type(B) == list) and ((type(X) != list) or (len(B) != len(X))):
			raise Exception()
		if (type(B) == int) or (type(B) == str):
			mat.set(self,self.index_of(A) if type(A) != int else A,self.index_of(B) if type(B) != int else B,X)
		else:
			self.connect(A,B[0],X[0])
			if len(B) > 1:
				self.connect(A,B[1:],X[1:])
		
	# Devuelve el coste entre los nodos A y B (A n dirección a B).
	# Devuelve A y B si A no está conectado con B
	def get(self,A,B):
		return mat.get(self,self.index_of(A) if type(A) != int else A,self.index_of(B) if type(B) != int else B)
		
	# Devuelve un valor booleano indicando si A está conectado con B
	# (dirección a B).
	def is_connected(self,A,B):
		return (self.get(A,B) != None)
		
	# Comprueba si existe la conexión A->B y B->A
	def is_fully_connected(self,A,B):
		return self.is_connected(A,B) and self.is_connected(B,A)

	# Devuelve todos los vecinos de un nodo dado.
	def get_neighbours(self, A):
		if not A in self.get_nodes():
			raise Exception()
		return filter(lambda B:self.is_connected(A,B),self.get_nodes())

	def map(self, func):
		otro = grafo(self.get_nodes())
		otro.from_list(mat.map(self, func).to_list())
		return otro

	def __str__(self):
		return mat.__str__(self)
		
	def __repr__(self):
		s = ' '.rjust(5) + ' '
		s = s + reduce(lambda x,y:x+y, map(lambda x:x.center(7), self.get_nodes()), '') + '\n'
		for i in range(0,self.get_width()):
			s = s + str(self.get_nodes()[i]).rjust(5)  + '|'
			for j in range(0,self.get_height()):
				s = s + (repr(round(self.get(i,j), 4) if type(self.get(i,j)) == float else self.get(i,j)).center(7) if self.get(i,j) != None else '---'.center(7))
			s = s + ' |\n'
		return s
