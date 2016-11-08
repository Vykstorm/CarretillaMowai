#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripci�n:
# Este m�dulo define el comportamiento del robot, que se divide en varias
# capas 

from moway_lib import moway
import motores, sensores

# Esta clase representa una m�quina de estados finitos.
class DTE:
	def __init__(self):
		self.estado_actual = self.inicio
	
	# Este m�todo modifica el estado actual.
	def cambiar_estado(self, otro_estado):
		print 'Cambiando estado: ' + self.estado_actual + ' -> ' + otro_estado
		self.estado_actual = otro_estado

	# Este m�todo inicia la m�quina de estados finitos.
	def ejecutar(self):
		while self.estado_actual != self.fin:
			self.estado_actual()
	
	# Estado inicial
	def inicio(self):
		cambiar_estado(self.fin)
		
	# Representa el estado final (la m�quina finaliza)
	def fin(self):
		pass
	
	
try:
	while True:
		zona, direccion = layer2.behaviour()
		layer1.behaviour(zona, direccion)
except KeyboardInterrupt:
	print 'Interrupci�n del teclado. Finalizando'
	moway.close_moway()
