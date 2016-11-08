#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# La clase ruta representa una ruta que debe seguir el robot.
# Será una secuencia de movimientos que debe realizar el robot hasta 
# llegar al final de la misma.

from collections import deque

class ruta:
	def __init__(self, movimientos):
		self.movimientos = deque(movimientos)
	
	# Este m�todo deber� devolver el siguiente movimiento a realizar.
	def siguiente_movimiento(self):
		if len(self.movimientos) == 0:
			return False
		movimiento = self.movimientos[0]
		self.movimientos.popleft()
		return movimiento
