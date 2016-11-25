#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripci�n:
# Este m�dulo define el comportamiento del robot con una m�quina de estados
# finitos (para seguir una ruta espec�fica)

from sensores import get_sensores, get_sensores_discretizados
from motores import move, girar, girar90, girar180, volver_atras
from ruta import estado, planificador_Aestrella
import mapa
from mapa import nodos, nodos_centro
from localizacion import gps

# Las instancias de esta clase representan  m�quinas de estados finitos.
class DTE:
	def __init__(self):
		pass
	
	# Este m�todo modifica el estado actual.
	def cambiar_estado(self, otro_estado):
		print 'Cambiando de estado: ' + self.estado_actual.__name__ + ' -> ' + otro_estado.__name__
		self.estado_actual = otro_estado
		
	# Este es un m�todo auxiliar que devolver� de forma continua las 
	# entradas que ser�n pasadas como par�metros a los m�todos que representan
	# los estados.
	def inputs(self):
		return ()

	# Este m�todo inicia la m�quina de estados finitos.
	def ejecutar(self):
		self.estado_actual = self.inicio
		while self.estado_actual != self.fin:
			self.estado_actual(*self.inputs())
	
	# Estado inicial
	def inicio(self, *args):
		self.cambiar_estado(self.fin)
		
	# Representa el estado final (la m�quina finaliza)
	def fin(self, *args):
		print 'Finalizando'
	

# La instancia de esta clase modelar� el comportamiento del robot moway como una m�quina de estados
# finitos.
class robot(DTE):
	# Pasamos como par�metro el estado inicial del robot (orientacion + posici�n) y el nodo destino.
	def __init__(self, inicio, destino, orientacion):
		DTE.__init__(self)
		
		# Planificamos la ruta inicial
		self.ruta = planificador_Aestrella(inicio, destino, orientacion).get_ruta()
		print 'Ruta inicial: ' + repr(self.ruta)
		print 'Siguiente movimiento: ' + repr(self.ruta.siguiente_movimiento())
		self.last_inputs = list(get_sensores_discretizados())
	
	def inputs(self):
		inputs = tuple(list(get_sensores_discretizados()) + self.last_inputs)
		self.last_inputs = list(get_sensores_discretizados())
		return inputs
		
        def cambiar_estado(self, otro_estado):
                if otro_estado == self.interseccion:
                        if not self.ruta.avanzar():  # El robot ha alcanzado su destino
                                self.cambiar_estado(self.fin) # Finalizar la ejecuci�n
                        else:
                                self.movimiento_actual = self.ruta.siguiente_movimiento()
                                print 'Siguiente movimiento: ' + repr(self.movimiento_actual)
                                # Nos metemos en el centro del tablero?
                                if self.ruta.estado_actual().get_nodo() in nodos_centro:
                                        robot_centro(self).ejecutar()				
                                DTE.cambiar_estado(self, otro_estado)
                else:
                        DTE.cambiar_estado(self, otro_estado)
	# Estado inicial.
        def inicio(self, *args):
                movimiento_actual = self.ruta.siguiente_movimiento()
                if movimiento_actual == 'left':
                        girar90('left')
                elif movimiento_actual == 'right':
                        girar90('right')
                elif movimiento_actual == 'forward':
                        pass
                self.cambiar_estado(self.transicion)
		
	# Estado pasillo
	def pasillo(self, ic, il, dc, dl, color, _ic, _il, _dc, _dl, *args):
		if color == 2: 
			self.cambiar_estado(self.interseccion)
		if (ic >= 1) and (dc >= 1):
                        print ic, dc, il, dl
                        if (ic == 2) and (dc == 2):
                                self.cambiar_estado(self.pasillo_bloqueado)
                        if (dl >= 1) and (il == 0):
                                self.cambiar_estado(self.esquina_izq)
                        elif (il >= 1) and (dl == 0):
                                self.cambiar_estado(self.esquina_der)
		else: 
			if (ic == 2) or (il == 2):
				girar('right')
			elif (dc == 2) or (dl == 2):
				girar('left')
			else:
				move()
   
	# Estado esquina izquierda
	def esquina_izq(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.interseccion)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo)
		else:
			if (ic == 2) or (dc == 2):
				girar('left')
			else:
				move()
				
	# Estado esquina derecha
	def esquina_der(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.interseccion)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo)
		else:
			if (ic == 2) or (dc == 2):
				girar('right')
			else:
				move()
	
	# Estado intersecci�n.
	def interseccion(self, ic, il, dc, dl, color, *args):
		if color < 2:
			self.cambiar_estado(self.pasillo)
		else:
                        movimiento_actual = self.ruta.siguiente_movimiento()
			if movimiento_actual == 'left':
				girar90('left')
				self.cambiar_estado(self.transicion)
			elif movimiento_actual == 'right':
				girar90('right')
				self.cambiar_estado(self.transicion)
			elif movimiento_actual == 'forward':
				move()
	def transicion(self, ic, il, dc, dl, color, *args):
		if color == 2:
			move()
		else:
			self.cambiar_estado(self.pasillo)

	# Estado bloqueado (obstaculo frontal en pasillo)
	def pasillo_bloqueado(self, ic, il, dc, dl, color, *args):
                # El robot da la vuelta
                girar180()
		
                # Vuelvo al nodo anterior y sigo la nueva ruta calculada
		self.cambiar_estado(self.pasillo_vuelta)
                
		orientacion_invertida = {'norte':'sur', 'sur':'norte', 'este':'oeste', 'oeste':'este'}
		estado_actual = self.ruta.estado_actual()
		estado_vuelta = estado(estado_actual.get_nodo(), orientacion_invertida[estado_actual.get_orientacion()])
		
		# Acualizamos la informaci�n del mapa (marcamos que hay un obst�culo obstruyendo
		# la ruta)
		mapa.obstaculos.block(estado_actual.get_nodo(), self.ruta.siguiente_estado().get_nodo())
		
		# Replanifico la ruta desde el �ltimo nodo.
		self.ruta = planificador_Aestrella(estado_vuelta.get_nodo(), self.ruta.estado_final().get_nodo(), estado_vuelta.get_orientacion()).get_ruta()
                print 'Ruta alternativa: ' + repr(self.ruta)
	

	# Estado pasillo vuelta
	def pasillo_vuelta(self, ic, il, dc, dl, color, _ic, _il, _dc, _dl, *args):
		if color == 2: 
			self.cambiar_estado(self.inicio)
		if (ic >= 1) and (dc >= 1):
                        if (ic == 2) and (dc == 2):
                                self.cambiar_estado(self.pasillo_bloqueado)
                        if (dl >= 1) and (il == 0):
                                self.cambiar_estado(self.esquina_izq)
                        elif (il >= 1) and (dl == 0):
                                self.cambiar_estado(self.esquina_der)
		else: 
			if (ic == 2) or (il == 2):
				girar('right')
			elif (dc == 2) or (dl == 2):
				girar('left')
			else:
				move()



# La instancia de esta clase modelar� el comportamiento del robot moway como una m�quina de estados
# finitos en el centro del tablero
# El comportamiento del robot en el centro del tablero es distinto (activa el algoritmo de localizaci�n).
# Para el resto del mapa, no es necesario activar dicho algoritmo.
class robot_centro(DTE):
	def __init__(self, parent):
		DTE.__init__(self)
		self.parent = parent
		print 'Entrando en la zona neutral. Nodo: ' + parent.ruta.estado_actual().get_nodo()
		self.localizador = gps(parent.ruta.estado_actual().get_nodo(), parent.ruta.estado_actual().get_orientacion())
                self.ultimo_nodo = self.localizador.get_nodo()
	# Inputs
	def inputs(self):
		return tuple([self.localizador.get_nodo()] + list(self.parent.inputs()))

	# Estado inicial.
	def inicio(self, *args):
		self.cambiar_estado(self.mover)
		# Activar algoritmo de localizaci�n.

	# Estado final
	def fin(self, *args):
                print 'Saliendo fuera de la zona neutral. Nodo: ' + self.ultimo_nodo

	# Estado mover

        
	# Estado final
	def final(self, *args):
		# Desactivar algoritmo de localizaci�n.
		pass
