#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Módulo para inicializar el robot (configurar el canal de radio) 

import sys
from time import sleep
sys.path.append("../lib/") # Añadimos la librería Moway
from moway_lib import moway


channel = 8  # Canal del robot moway.

# Configuramos el canal moway
print "Configurando el robot moway..."
if moway.init_prog_moway() == 0:
	print "Bateria del moway: " , moway.read_moway_batt()
	if moway.program_moway_channel("../lib/moway.hex",channel) == 0 :
		print("Moway programado con exito")
	else :
		print("Error programando el robot")
moway.exit_moway()
