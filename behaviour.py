#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Este módulo define el comportamiento del robot con una máquina de estados
# finitos (para seguir una ruta específica)

from sensores import get_sensores, get_sensores_discretizados
from motores import move, girar

# Las instancias de esta clase representan  máquinas de estados finitos.
class DTE:
	def __init__(self):
		pass
	
	# Este método modifica el estado actual.
	def cambiar_estado(self, otro_estado):
		print 'Cambiando de estado: ' + self.estado_actual.__name__ + ' -> ' + otro_estado.__name__
		self.estado_actual = otro_estado
		
	# Este es un método auxiliar que devolverá de forma continua las 
	# entradas que serán pasadas como parámetros a los métodos que representan
	# los estados.
	def inputs(self):
		return ()

	# Este método inicia la máquina de estados finitos.
	def ejecutar(self):
		self.estado_actual = self.inicio
		while self.estado_actual != self.fin:
			self.estado_actual(*self.inputs())
	
	# Estado inicial
	def inicio(self, *args):
		self.cambiar_estado(self.fin)
		
	# Representa el estado final (la máquina finaliza)
	def fin(self, *args):
		print 'Finalizando'
	

# La instancia de esta clase modelará el comportamiento del robot moway como una máquina de estados
# finitos.
class robot(DTE):
	# Pasamos como parámetro la ruta que deberá llevar el robot moway 
	def __init__(self, ruta):
		DTE.__init__(self)
		self.ruta = ruta
		self.last_inputs = list(get_sensores_discretizados())
	
	def inputs(self):
		inputs = tuple(list(get_sensores_discretizados()) + self.last_inputs)
		self.last_inputs = list(get_sensores_discretizados())
		return inputs
		
	def cambiar_estado(self, otro_estado):
		DTE.cambiar_estado(self, otro_estado)
		if otro_estado == self.interseccion: 
			self.movimiento_actual = self.ruta.siguiente_movimiento() # Siguiente movimiento ?
			if not self.movimiento_actual:  # El robot ha alcanzado su destino
				self.cambiar_estado(self.fin) # Finalizar la ejecución
			else:
				print 'Siguiente movimiento: ' + self.movimiento_actual
	
	# Estado inicial.
	def inicio(self, *args):
		self.cambiar_estado(self.pasillo)
		
	# Estado pasillo
	def pasillo(self, ic, il, dc, dl, color, _ic, _il, _dc, _dl, *args):
		if color == 2: 
			self.cambiar_estado(self.interseccion)
		if (ic >= 1) and (dc >= 1):
                        if (dl >= 1) and (il == 0):
                                self.cambiar_estado(self.esquina_izq)
                        elif (il >= 1) and (dl == 0):
                                self.cambiar_estado(self.esquina_der)
		else: 
			if (ic == 2) or (il == 2):
				girar('right')
			elif (dc == 2) or (dl == 2):
				girar('left')
			else:
				move()	
		
	# Estado esquina izquierda
	def esquina_izq(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.interseccion)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo)
		else:
			if (ic == 2) or (dc == 2):
				girar('left')
			else:
				move()
				
	# Estado esquina derecha
	def esquina_der(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.interseccion)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo)
		else:
			if (ic == 2) or (dc == 2):
				girar('right')
			else:
				move()
	
	# Estado intersección.
	def interseccion(self, ic, il, dc, dl, color, *args):
		if color < 2:
			self.cambiar_estado(self.pasillo)
		else:
			if self.movimiento_actual == 'left':
				girar('left')
			elif self.movimiento_actual == 'right':
				girar('right')
			elif self.movimiento_actual == 'forward':
				move()

