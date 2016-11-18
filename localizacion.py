#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de rutinas para localizar el robot
# dentro de un tablero (con forma de malla).


from matriz import matriz
from thread import start_new_thread
from threading import Condition
from time import sleep
from sensores import get_sensores_discretizados, get_dist_recorrida


# Este método aplica un filtro laplaciando sobre una lista de valores númericos
# enteros. Por ejemplo, si se le pasa [1 2 3], el método devolvería los valores
# 1+1 / 6+3, 2+1 / 6+3, 3+1 / 6+3
def laplace(v):
        s = float(sum(v) + len(v))
        return map(lambda x:x/s, map(lambda x:x+1, v))


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
        m = matriz(*p.get_size())
        m.from_list(reduce(lambda x,y:x+y, map(lambda r:shift(r, x), p.get_rows()), []))
        return m
        

# Igual pero por columnas.
def shift_cols(p, x):
        m = matriz(*p.get_size())
        for j, c in map(lambda j,r:(j,shift(r, x)), range(0,p.get_height()), p.get_cols()):
			m.set_col(j, c)
        return m

## Funciones para el calculo de probabilidades y la localización del robot.
# Cada casilla tendrá asociada una probabilidad.
# Estimaremos la posición actual del robot, busquando la casilla con mayor probabilidad.


# Este método inicializa las probabilidades de las casillas. Debe indicarse la
# posición del robot en el tablero. La probabilidad de dicha casilla será 1, y el
# resto será cero, pero se aplicará un filtro laplaciano para suavizar los valores.
# Después de invocar este método se actualizarán las probabilidades del tablero cada cierto
# tiempo. También debe indicarse la dirección del movimiento del robot ['norte', 'sur', 'este', 'oeste']
def iniciar_localizacion(i, j, direccion):
        global grid, actualizar, direccion_movimiento
        with grid_lock:
                # Inicializamos la matriz de probabilidades
                p = grid
                p.from_list([0] * (p.get_width() * p.get_height()))
                p[i,j] = 8
                # Aplicamos filtro laplaciano
                p.from_list(laplace(p.to_list()))

                # Comenzamos a actualizar la matriz de probabilidades
                actualizar = True
                direccion_movimiento = direccion
                grid_lock.notify()
                


# Para la localización del robot en el tablero (las probabilidades dejan de actualizarse).
def parar_localizacion():
        global actualizar
        with grid_lock:
                actualizar = False
                grid_lock.notify()

# Este método recalcula las probabilidades de las casillas (son probabilidades condicionales
# que dependen de las variables observables)
def recalcular():
        global grid, color_grid
        p = grid # Matriz con las probabilidades a priori
        
	ic, il, dc, dl, color = get_sensores_discretizados()
	negro = (color == 2)
	blanco = (color < 2)
	
	# Calculamos las probabilidades P(vB | C11), P(vB | C12), ...
	pInv = p.map(lambda pPriori,i,j:0.8*(color_grid[i,j] == blanco)+0.1*(color_grid[i,j] != blanco))

        # Calculamos la probabilidades P(C11 | vB), P(C12 |vB), ...
        p.from_list(bayes(pInv.to_list(), p.to_list()))

        print 'color: ' + repr(blanco)


# Este método actualiza las probabilidades de las casillas (las desplaza), en base a la distancia
# recorrida desde la ultima actualización.
def desplazar():
        global grid
        p = grid
        d = get_dist_recorrida()
        
        u = 10*d / 150.0 # nº casillas recorridas desde la última actualización.
        y = 0.2 # La incertidumbre de moverse una casilla hacia delante es del x%
        x = min(u,1) * (1 - y)

        if direccion_movimiento == 'este':
                p = shift_rows(p, x)

        for i in range(0, p.get_width()):
                for j in range(0, p.get_height()):
                        if p[i,j] == max(p.to_list()):
                                print 'pos: ' + repr(i) + ", " + repr(j)
        print repr(p)
        
# Estas variables establecen las dimensiones del tablero.
GRID_WIDTH = 3
GRID_HEIGHT = 3

# Esta matriz guarda las probabilidades de cada casilla
grid = matriz(GRID_WIDTH, GRID_HEIGHT)

# Esta matriz almacena el color real de cada casilla (1 blanco, 0 negro)
color_grid = matriz(GRID_WIDTH, GRID_HEIGHT)
color_grid[0] = [1, 0, 1]
color_grid[1] = [0, 1, 0]
color_grid[2] = [1, 0, 1]

grid_lock = Condition()
actualizar = False
direccion_movimiento = 'este'

POSITION_UPDATE_TIME = 1
def actualiza_localizacion():
        global grid
        while True:
                grid_lock.acquire()
                while not actualizar:
                        grid_lock.wait()
                with grid_lock:
                        # Recalculamos las probabilidades.
                        recalcular()
                        # Desplazamos las probabilidades.
                        desplazar()
                        grid_lock.wait(POSITION_UPDATE_TIME)


start_new_thread(actualiza_localizacion, ())

