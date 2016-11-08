#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Define el comportamiento del robot en la capa 1. 
# La capa 1 establece la forma en la que el robot debe moverse en distintos escenarios, sin chocarse
# con ningún obstáculo o pared.

from motores import cambiar_direccion, move, girar
from sensores import get_sensores, get_sensores_discretizados
from time import sleep
from moway_lib import moway

def behaviour(zona, direccion):
	ic, il, dc, dl, color = get_sensores_discretizados()
        
	if zona == 'esquina': # Comportamiento del robot en una esquina
		if (ic == 2) or (dc == 2):
				girar(direccion)
		else:
				move()
	elif zona == 'pasillo': # Comportamiento del robot en un pasillo
		if (ic == 2) or (il == 2):
				girar('right')
		elif (dc == 2) or (dl == 2):
				girar('left')
		else:
				move()
	elif zona == 'interseccion': # Comportamiento del robot en una intersección.
		if direccion == 'forward':
			move()
		elif direccion == 'left':
			girar('left')
		elif direccion == 'right':
			girar('right')
          
