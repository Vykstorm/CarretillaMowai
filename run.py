#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Módulo para iniciar y comenzar a mover el robot



# Inicializamos el robot
import atexit, sys
sys.path.append("../lib/")
from moway_lib import moway, exit_mow
from behaviour import robot
from ruta import ruta

print "Inicializando el robot moway..."
if __name__ == '__main__':
        atexit.register(exit_mow)
	
channel = 8
moway.usbinit_moway() 
ret = moway.init_moway(channel)

if ret == 0:
	print 'Moway conectado con exito...'
else:	
	print 'Error al conectar el moway...'
	exit(-1)

# Comenzamos a ejecutar el código para mover el robot...
			
try:
	# Creamos una ruta que deba seguir el robot.
	R = ruta(['left', 'forward', 'left', 'right', 'forward']) 
	
	# Comenzamos a mover el robot
	robot(R).ejecutar()
	print 'Movimiento del robot finalizado'
except KeyboardInterrupt:
	print 'Interrupción del teclado. Finalizando'
finally:
	moway.close_moway()
	print 'Apagando robot'
