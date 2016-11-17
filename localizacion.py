



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


