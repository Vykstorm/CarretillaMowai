#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Módulo que define una serie de rutinas que llevan acabo las siguientes tareas:
# - Tratamiento de la incertidumbre en los datos de los sensores de infrarrojos.
# - Conversión de unidades de los sensores de infrarrojos a medidas de distancia (cm)

# Módulos importados
from collections import deque
from math import pi, sqrt, exp
import thread
from time import sleep
from random import random
import moway_input

	

# Almacenar registros con las anteriores mediciones de cada sensor.
MAX_LENGTH_SENSOR_REG = 4 # Número de mediciones consecutivas a almacenar por cada sensor.
mediciones = dict(map(lambda sensor:(sensor, deque(maxlen=MAX_LENGTH_SENSOR_REG)), ['izq_central', 'izq_lateral', 'der_central', 'der_lateral']));

# Funciones que devuelve por cada sensor una lista de valores de sus anteriores mediciones, más
# la medición actual de cada uno.

def _sensor_izq_central():
	valores = mediciones['izq_central']
	valores.appendleft(moway_input.sensor_izq_central())
	return valores

def _sensor_izq_lateral():
	valores = mediciones['izq_lateral']
	valores.appendleft(moway_input.sensor_izq_lateral())
	return valores
	
def _sensor_der_lateral():
	valores = mediciones['der_central']
	valores.appendleft(moway_input.sensor_der_central())
	return valores
	
def _sensor_der_central():
	valores = mediciones['der_lateral']
	valores.appendleft(moway_input.sensor_der_lateral())
	return valores
	
# Métodos para agregar una secuencia de mediciones consecutivas de un sensor y 
# devolver un unico valor (que puede usarse para aproximar el valor real actual
# del sensor)


def agregar_mediciones(valores):
	return media(valores)
	
def media(valores):
	return sum(valores) / len(valores);





# Métodos para eliminar outliers: valores del sensor extremadamente grandes o pequeños 
# en relación a mediciones anteriores (los consideramos como errores del sensor)


# Esta función devuelve un rango entre los cuales se encontrará el 80% de valores que
# siguen una distribución normal estándar en torno a su media.
def zvalues(mu, s):
	return  [c*s + mu for c in [-1.2816, 1.2816]]


# Funcion para calcular desviacion estándar de un conjunto de mediciones.
def sigma(valores, mu):
	return sqrt(sum([(x-mu)**2.0 for x in valores]) / (len(valores)-1))
	 

def eliminar_outliers(valores):
	if len(valores) < 5: # si hay pocos valores, no marcamos a ninguno como outliers 
		return valores
	mu = media(valores)
	s = sigma(valores, mu)
	z = zvalues(mu, s)
	check_outlier = lambda v: (v >= z[0]) and (v <= z[1])
	valores_filtrados = filter(check_outlier, valores)
	return valores_filtrados
	

# Funciones que devuelven la medición actual real aproximada del sensor, eliminando
# outliers y agregando mediciones consecutivas.

def sensor_izq_central_rectified():
	return agregar_mediciones(eliminar_outliers(_sensor_izq_central()))

def sensor_izq_lateral_rectified():
	return agregar_mediciones(eliminar_outliers(_sensor_izq_lateral()))

def sensor_der_central_rectified():
	return agregar_mediciones(eliminar_outliers(_sensor_der_central()))

def sensor_der_lateral_rectified():
	return agregar_mediciones(eliminar_outliers(_sensor_der_lateral()))




# Función para discretizar los valores de los sensores, en
# valores categóricos:
# 0 = bajo (cuando el sensor da una medición baja)
# 1 = medio, (cuando el sensor da una medición intermedia)
# 2 = alto, (cuando el sensor da una medición alta)
def discretizar(vic, vil, vdc, vdl):
        def discretizar_central(x):
                if x >= .52:
                        return 2
                elif x <= 0.12:
                        return 0
                return 1
        def discretizar_lateral(x):
                if x >= .72:
                        return 2
                elif x <= 0.12:
                        return 0
                return 1
        return (discretizar_central(vic), discretizar_lateral(vil), discretizar_central(vdc), discretizar_lateral(vdl))
# .72, .12

# Se crea un hilo de ejecución asíncrono que vaya obteniendo información de los
# sensores cada cierto tiempo. 		

sensores = dict(zip(['izq_central', 'izq_lateral', 'der_central', 'der_lateral'], map(lambda x:x(), [sensor_izq_central_rectified, sensor_izq_lateral_rectified, sensor_der_central_rectified, sensor_der_lateral_rectified])))
def actualizar_mediciones(update_time):
	while True: 
		with sensores_lock:
			sensores.update(dict(zip(['izq_central', 'izq_lateral', 'der_central', 'der_lateral'], map(lambda x:x(), [sensor_izq_central_rectified, sensor_izq_lateral_rectified, sensor_der_central_rectified, sensor_der_lateral_rectified]))))
		sleep(update_time / 1000.0)
		
	
SENSOR_UPDATE_TIME = 5
sensores_lock = thread.allocate_lock()
thread.start_new_thread(actualizar_mediciones, (SENSOR_UPDATE_TIME,))







## Interfaz.

# Métodos que devuelven las mediciones de los sensores actualmente.

def sensor_izq_central():
        with sensores_lock:
                valor = sensores['izq_central']
        return valor
        
def sensor_der_central():
        with sensores_lock:
                valor = sensores['der_central']
        return valor

def sensor_izq_lateral():
        with sensores_lock:
                valor = sensores['izq_lateral']
        return valor

def sensor_der_lateral():
        with sensores_lock:
                valor = sensores['der_lateral']
        return valor

def get_sensores():
        with sensores_lock:
                valores = (sensores['izq_central'], sensores['izq_lateral'], sensores['der_central'], sensores['der_lateral'])
	return valores



