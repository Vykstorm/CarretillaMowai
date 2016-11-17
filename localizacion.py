#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de rutinas para localizar el robot
# dentro de un tablero (con forma de malla).


from matriz import matriz
from thread import start_new_thread, allocate_lock
from time import sleep
from sensores import get_sensores_discretizados, get_dist_recorrida

# Esta funcion calcula un conjunto de probabilidades condicionadas usando
# el teorema de bayes sencillo.
# Sean x1, x2, ... xN las variables no observables e y la variable observable
# Devueleve la lista de prob. condicionadas: P(x1 | y), P(x2 | y), ... P(xN | y)
# Toma los siguientes parametros:
# La lista de probs. condicionadas invertidas:
# P(y | x1), P(y | x2), ..., P(y | xN) y las probabilidades a priori:
# P(x1), P(x2), ... P(xN)
def bayes(pInv, pPriori):
	pTotal = sum(map(lambda x,y:x*y, pInv, pPriori))
	return map(lambda x,y:(x*y)/pTotal, pInv, pPriori)


# Esta funcion mueve un conjunto de probabilidades, de forma que:
# La casilla P(i)' = x * P(i-1) + (1-x) * P(i) 
def shift(p, x):
	return map(lambda a,b:a+b, map(lambda y:y*x, ([0] + p[:-1])), map(lambda y:y*(1-x), p))


# Esta función es igual que la anterior solo que lo hace para cada fila
# de una matriz. Devuelve una matriz nueva con las probabilidades desplazadas.
def shift_rows(p, x):
        nr = map(lambda r:shift(r, x), [p.get_row(i) for i in range(0,p.get_rows())])
        m = matriz(p.get_rows(), p.get_cols())
        for i in range(p.get_rows()):
                m.set_row(i,nr[i])
        return m

# Igual pero por columnas.
def shift_cols(p, x):
        nc = map(lambda c:shift(c, x), [p.get_col(j) for j in range(0,p.get_cols())])
        m = matriz(p.get_rows(), p.get_cols())
        for j in range(p.get_cols()):
                m.set_col(j,nc[j])
        return m  

## Funciones para el calculo de probabilidades y la localización del robot.
# Cada casilla tendrá asociada una probabilidad.
# Estimaremos la posición actual del robot, busquando la casilla con mayor probabilidad.

# Este método recalcula las probabilidades de las casillas (son probabilidades condicionales
# que dependen de las variables observables, que son la distancia recorrida y el color)
def recalcular(grid):
        pass
def desplazar(grid):
        pass


GRID_WIDTH = 3
GRID_HEIGHT = 3
grid = matriz(GRID_WIDTH, GRID_HEIGHT) # Esta matriz guarda las probabilidades de cada casilla
color_grid = matriz(GRID_WIDTH, GRID_HEIGHT) # Esta matriz almacena el color de cada casilla

color_grid[0] = [1, 0, 1]
color_grid[1] = [0, 1, 0]
color_grid[2] = [1, 0, 1]


grid_lock = allocate_lock()




POSITION_UPDATE_TIME = 1
def actualiza_localizacion():
        global grid
        while True:
                with grid_lock:
                        # Recalculamos las probabilidades.
                        grid = recalcular(grid)
                        # Desplazamos las probabilidades.
                        grid = desplazar(grid)
                sleep(POSITION_UPDATE_TIME)


start_new_thread(actualiza_localizacion, ())


