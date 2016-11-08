#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Este módulo define el comportamiento del robot, que se divide en varias
# capas 

from moway_lib import moway
import motores, sensores

# Esta clase representa una máquina de estados finitos.
class DTE:
	def __init__(self):
		self.estado_actual = self.inicio
	
	# Este método modifica el estado actual.
	def cambiar_estado(self, otro_estado):
		print 'Cambiando estado: ' + self.estado_actual + ' -> ' + otro_estado
		self.estado_actual = otro_estado

	# Este método inicia la máquina de estados finitos.
	def ejecutar(self):
		while self.estado_actual != self.fin:
			self.estado_actual()
	
	# Estado inicial
	def inicio(self):
		cambiar_estado(self.fin)
		
	# Representa el estado final (la máquina finaliza)
	def fin(self):
		pass
	
	
try:
	while True:
		zona, direccion = layer2.behaviour()
		layer1.behaviour(zona, direccion)
except KeyboardInterrupt:
	print 'Interrupción del teclado. Finalizando'
	moway.close_moway()
