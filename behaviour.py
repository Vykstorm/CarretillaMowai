#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Módulo que define una serie de métodos para poder implementar las capas
# de nuestra arquitectura de subsumción (implementación de dos máquinas de estados
# finitos que modelen el comportamiento del robot)

import motores, sensores
from sensores import get_sensores, discretizar
from motores import cambiar_direccion, move, girar
from time import sleep
from moway_lib import moway

# Estado inicial
def controlador():
	ic, il, dc, dl = discretizar(*get_sensores())
                
	
        if zona == 'esquina':
                if (ic == 2) or (dc == 2):
                        girar(hueco)
                else:
                        move()
        elif zona == 'pasillo':
                if (ic == 2) or (il == 2):
                        girar('right')
                elif (dc == 2) or (dl == 2):
                        girar('left')
                else:
                        move()
                        



# Esta variable indica la zona en la que se encuentra el
# el robot, que puede ser pasillo, interseccion o esquina
zona = 'esquina'

# Esta variable indica hacia donde debe girar el robot en el
# caso en el que se encuentre en una esquina
hueco = 'left'



try:
        while True:
                controlador()
except KeyboardInterrupt:
        print 'Interrupci�n del teclado. Finalizando'
        moway.close_moway()
