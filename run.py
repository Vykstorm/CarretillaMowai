#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Módulo para iniciar y comenzar a mover el robot



# Inicializamos el robot
import atexit, sys
sys.path.append("../lib/")
from moway_lib import moway, exit_mow

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
import behaviour
