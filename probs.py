#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de métodos para trabajar y 
# calcular probabilidades

import matriz


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
