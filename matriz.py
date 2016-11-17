#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Este script define una representación de una matriz.


class matriz:
	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.valores = ([[0] * m]) * n
		self.valores = []
		for i in range(0,n):
			self.valores.append([0] * m)
	def get_rows(self):
		return self.n
		
	def get_cols(self):
		return self.m
		
	def get(self, i,j):
		return self.valores[i][j]
	
	def set(self, i,j, x):
		self.valores[i][j] = x
	
	def get_row(self, i):
		return self.valores[i][:]
			
	def get_col(self, j):
		return list(zip(self.valores)[j])
		
	def set_row(self, i, r):
		self.valores[i] = r
		
	def set_col(self, j, r):
		pass
	
	def __getitem__(self, indexes):
		if type(indexes) == int:
			return self.get_row(indexes)
		i, j = indexes
		return self.get(i,j)
	
	def __setitem__(self, indexes, x):
		if type(indexes) == int:
			self.set_row(indexes, x)
		else: 
			i, j = indexes
			self.set(i,j,x)
		
	def __str__(self):
		return self.valores.__str__()

m = matriz(3,3)
print m[0][0]
