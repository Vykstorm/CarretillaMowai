#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Este script define una representación de una matriz.

from exceptions import IndexError
from copy import copy, deepcopy

class matriz:
	# Constructor.
	# Inicializa una matriz nxm con ceros
	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.valores = map(lambda x:[x]*m, [0] * n) 
			
	# Construye una matriz a partir de una lista
	# de valores. Si M es la matriz y L es la lista ->
	# M[i][j] = L[i*cols + j]
	def from_list(self,l):
		if (len(self) != len(l)):
			raise Exception()
		self.valores = map(lambda k:l[k:k+self.m], [i * self.m for i in range(0,self.n)])
		
	# Devuelve los elementos de la matriz en una sola lista.
	# Donde L[k] = M[k / cols, k % cols]
	def to_list(self):
		return reduce(lambda x,y: x + y, self.valores,[])
			
	# Devuelve el num filas de la matriz
	def get_width(self):
		return self.n
		
	# Devuelve el número de columnas de la matriz
	def get_height(self):
		return self.m
		
	# Devuelve el tamaño de la matriz
	def get_size(self):
		return (self.get_width(), self.get_height())
		
	# Devuelve el elemento en la posición (i,j)
	def get(self, i,j):
		if (i<0) or (i>=self.n) or (j<0) or (j>=self.m):
			raise IndexError()
		return self.valores[i][j]
	
	# Establece el valor del elemnto en la posición (i,j)
	def set(self, i,j, x):
		if (i<0) or (i>=self.n) or (j<0) or (j>=self.m):
			raise IndexError()
		self.valores[i][j] = x
	
	# Devuelve una copia de la fila i-ésima
	def get_row(self, i):
		if (i<0) or (i>=self.n):
			raise IndexError()
		return copy(self.valores[i])
			
	# Devuelve una copia de la fila j-ésima
	def get_col(self, j):
		if (j<0) or (j>=self.m):
			raise IndexError()
		return map(lambda r:r[j], self.valores)
		
	# Devuelve una lista con las filas de la matriz
	def get_rows(self):
		return deepcopy(self.valores)
		
	# Devuelve una lista con las columnas de la matriz
	def get_cols(self):
		return [map(lambda r:r[j], self.valores) for j in range(0, self.m)]
		
	# Establece los valores de la fila i-ésima
	def set_row(self, i, r):
		if (i<0) or (i>=self.n):
			raise IndexError()
		self.valores[i] = copy(r)
		
	# Establece los valores de la fila j-ésima
	def set_col(self, j, r):
		for i in range(0, self.n):
                        self.set(i,j, r[i])
	# Realiza una operación por cada elemento  de la matriz, y devuelve 
	# el resultado de invocar una función por cada elemento en forma de otra
	# matriz
	def map(self, func):
		otra = matriz(self.n, self.m)
		otra.from_list(map(lambda v,pos:func(v,*pos),  self.to_list(), [(i,j) for i in range(0,self.n) for j in range(0,self.m)] ))
		return otra
	
	# Devuelve el número de elementos totales de la matriz (nxm)
	def __len__(self):
		return self.n * self.m
	
	# Operador de indexación 
	def __getitem__(self, indexes):
		if type(indexes) == int:
			i = indexes
			if (i<0) or (i >= self.n):
				raise IndexError()
			return self.get_row(i)
		if (i < 0) or (i >= self.n) or (j < 0) or (j >= self.m):
			raise IndexError()
		i, j = indexes
		return self.get(i,j)
	
	# Operador de indexación-asignación
	def __setitem__(self, indexes, x):
		if type(indexes) == int:
			i = indexes
			if (i<0) or (i >= self.n):
				raise IndexError()
			self.set_row(i, x)
		else: 
			i, j = indexes
			if (i < 0) or (i >= self.n) or (j < 0) or (j >= self.m):
				raise IndexError()
			self.set(i,j,x)
		
	# Devuelve un iterador para iterar sobre los elementos
	# de la matriz
	def __iter__(self):
		return iter(self.to_list())
		
	# Devuelve una representación de la matriz en
	# forma de sring.
	def __str__(self):
		return self.valores.__str__()
		
	def __repr__(self):
		s = ''
		for i in range(0,self.n):
			s = s + '|'
			for j in range(0,self.m):
				s = s + repr(self.get(i,j)).center(12)
			s = s + ' |\n'
		return s

# Alias de clase
mat = matriz
