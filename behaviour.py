#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripci�n:
# Este m�dulo define el comportamiento del robot, que se divide en varias
# capas 

from moway_lib import moway
import motores, sensores
import layer1, layer2

try:
	layer2.behaviour()
	layer1.behaviour()
except KeyboardInterrupt:
	print 'Interrupci�n del teclado. Finalizando'
	moway.close_moway()
