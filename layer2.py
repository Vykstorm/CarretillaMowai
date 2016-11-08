#!/usr/bin/python
	# -*- coding: iso8859-1 -*-
# Descripción: Esta capa modifica el comportamiento del robot en la capa 1. 
# Esta capa se analizar la información de los sensores y determinar en 
# que zona se encuentra el robot (en un pasillo, zona o intersección) además

from motores import cambiar_direccion, move, girar
from sensores import get_sensores, get_sensores_discretizados





def behaviour():
        global _ic, _il, _dc, _dl
        global zona, direccion
        ic, il, dc, dl, color = get_sensores_discretizados()

        if zona == 'pasillo':
                if color == 2:
                        zona = 'interseccion'
                        direccion = 'left'
                elif (_il > 0) and (il == 0):
                        zona, direccion = 'esquina', 'left'
                elif (_dl > 0) and (dl == 0):
                        zona, direccion = 'esquina', 'right'
        elif zona == 'interseccion':
                if color < 2:
                        zona = 'pasillo'
        elif (zona == 'esquina') and (direccion == 'left'):
                if color == 2:
                        zona = 'interseccion'
                        direccion = 'left'
                elif (ic == 0) and (dc == 0):
                        zona = 'pasillo'
        elif (zona == 'esquina') and (direccion == 'right'):
                if color == 2:
                        zona = 'interseccion'
                        direccion = 'left'
                elif (ic == 0) and (dc == 0):
                        zona = 'pasillo'

        _ic, _il, _dc, _dl = ic, il, dc, dl

	return (zona, direccion)

# Estas variables almacenan las mediciones de los sensores discretizadas
# en el instante anterior
_ic, _il, _dc, _dl, _ = get_sensores_discretizados()

zona, direccion = 'pasillo', 'left'
