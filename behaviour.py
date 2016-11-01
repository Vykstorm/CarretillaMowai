#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Este módulo define el comportamiento del robot, que se divide en varias
# capas 

from moway_lib import moway
import motores, sensores
import layer1, layer2

try:
	layer2.behaviour()
	layer1.behaviour()
except KeyboardInterrupt:
	print 'Interrupción del teclado. Finalizando'
	moway.close_moway()
