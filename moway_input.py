#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripci�n:
# M�dulo que define m�todos que llaman a rutinas de la librer�a moway para
# obtener informaci�n de los sensores (métodos wrapper)

from moway_lib import moway




# Wrappers para obtener informaci�n de los sensores (pero devuelve valores normalizados 
# en el rango [0, 1]
def sensor_izq_central():
	return moway.get_obs_center_left()/100.0;

def sensor_izq_lateral():
	return moway.get_obs_side_left()/100.0;
	
def sensor_der_central():
	return moway.get_obs_center_right()/100.0;
	
def sensor_der_lateral():
	return moway.get_obs_side_right()/100.0;

def sensor_color():
	return min(moway.get_line_right() + moway.get_line_left(), 100)/100.0;
