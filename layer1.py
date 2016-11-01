#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Define el comportamiento del robot en la capa 1. 
# La capa 1 establece la forma en la que el robot debe moverse en distintos escenarios, sin chocarse
# con ningún obstáculo o pared.

from motores import cambiar_direccion, move, girar
from sensores import get_sensores, discretizar


def behaviour():
	ic, il, dc, dl, color = discretizar(*get_sensores())
                
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
          
                        
# Variables auxiliares.

# Indica la zona en la que se encuentra el robot. En función de este el robot
# seguirá un comportamiento u otro.
zona = 'esquina'

# Esta variable tiene varios usos. Si el robot se encuentra en una esquina,
# esta debe indicar el sentido hacia donde debe girar el robot para seguir su
# camino: Hacia la izquierda 'left' o hacia la derecha 'right'
# Si el robot esta en una intersección, puede tomar los valores 'forward', 'left' o
# 'right' , en función de si debe tomar el camino de la izquierda, derecha o 
# hacia delante.
direccion = 'left'


