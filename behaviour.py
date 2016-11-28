#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Este módulo define el comportamiento del robot con una máquina de estados
# finitos (para seguir una ruta específica)

from sensores import get_sensores, get_sensores_discretizados
from motores import move, girar, girar90, girar180, volver_atras, stop
from ruta import estado, planificador_Aestrella
import mapa
from mapa import nodos, nodos_centro
from localizacion import gps
from time import sleep

# Las instancias de esta clase representan  máquinas de estados finitos.
class DTE:
	def __init__(self):
		pass
	
	# Este método modifica el estado actual.
	def cambiar_estado(self, otro_estado):
		print 'Cambiando de estado: ' + self.estado_actual.__name__ + ' -> ' + otro_estado.__name__
		self.estado_actual = otro_estado
		
	# Este es un método auxiliar que devolverá de forma continua las 
	# entradas que serán pasadas como parámetros a los métodos que representan
	# los estados.
	def inputs(self):
		return ()

	# Este método inicia la máquina de estados finitos.
	def ejecutar(self):
		self.estado_actual = self.inicio
		while self.estado_actual != self.fin:
			self.estado_actual(*self.inputs())
		self.fin(*self.inputs())
	
	# Estado inicial
	def inicio(self, *args):
		self.cambiar_estado(self.fin)
		
	# Representa el estado final (la máquina finaliza)
	def fin(self, *args):
		print 'Finalizando'
	

# La instancia de esta clase modelará el comportamiento del robot moway como una máquina de estados
# finitos.
class robot(DTE):
	# Pasamos como parámetro el estado inicial del robot (orientacion + posición) y el nodo destino.
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
                                self.cambiar_estado(self.fin) # Finalizar la ejecución
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
                #print il, _il
		if color == 2: 
			self.cambiar_estado(self.interseccion)
		elif (ic >= 1) and (dc >= 1):
                        if ((ic == 2) or (dc == 2)) and (il >= 1) and (dl >= 1):
                                self.cambiar_estado(self.pasillo_bloqueado)
                        if (dl >= 1) and (il == 0):
                                self.cambiar_estado(self.esquina_izq)
                        elif (dl == 0) and (il >= 1):
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
		elif ((ic == 2) and (dc == 2)) and (il == 2) and (dl == 2):
                        self.cambiar_estado(self.pasillo_bloqueado)
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
		elif ((ic == 2) and (dc == 2)) and (il == 2) and (dl == 2):
                        self.cambiar_estado(self.pasillo_bloqueado)
		else:
			if (ic == 2) or (dc == 2):
				girar('right')
			else:
				move()
	
	# Estado intersección.
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
		
		# Acualizamos la información del mapa (marcamos que hay un obstáculo obstruyendo
		# la ruta)
		mapa.obstaculos.block(estado_actual.get_nodo(), self.ruta.siguiente_estado().get_nodo())
		
		# Replanifico la ruta desde el último nodo.
		self.ruta = planificador_Aestrella(estado_vuelta.get_nodo(), self.ruta.estado_final().get_nodo(), estado_vuelta.get_orientacion()).get_ruta()
                print 'Ruta alternativa: ' + repr(self.ruta)
	

	# Estado pasillo vuelta
	def pasillo_vuelta(self, ic, il, dc, dl, color, _ic, _il, _dc, _dl, *args):
		if color == 2: 
			self.cambiar_estado(self.inicio)
		elif (ic >= 1) and (dc >= 1):
                        if ((ic == 2) or (dc == 2)) and (il >= 1) and (dl >= 1):
                                self.cambiar_estado(self.pasillo_bloqueado)
                        if (dl >= 1) and (il == 0):
                                self.cambiar_estado(self.esquina_izq_vuelta)
                        elif (dl == 0) and (il >= 1):
                                self.cambiar_estado(self.esquina_der_vuelta)
		else:
			if (ic == 2) or (il == 2):
				girar('right')
			elif (dc == 2) or (dl == 2):
				girar('left')
			else:
				move()


	# Estado esquina izquierda de 
	def esquina_izq_vuelta(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.inicio)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo_vuelta)
		elif ((ic == 2) and (dc == 2)) and (il == 2) and (dl == 2):
                        self.cambiar_estado(self.pasillo_bloqueado)
		else:
			if (ic == 2) or (dc == 2):
				girar('left')
			else:
				move()
				
	# Estado esquina derecha
	def esquina_der_vuelta(self, ic, il, dc, dl, color, *args):
		if color == 2:
			self.cambiar_estado(self.inicio)
		elif (ic == 0) and (dc == 0):
			self.cambiar_estado(self.pasillo_vuelta)
		elif ((ic == 2) and (dc == 2)) and (il == 2) and (dl == 2):
                        self.cambiar_estado(self.pasillo_bloqueado)
		else:
			if (ic == 2) or (dc == 2):
				girar('right')
			else:
				move()
				


# La instancia de esta clase modelará el comportamiento del robot moway como una máquina de estados
# finitos en el centro del tablero
# El comportamiento del robot en el centro del tablero es distinto (activa el algoritmo de localización).
# Para el resto del mapa, no es necesario activar dicho algoritmo.
class robot_centro(DTE):
	def __init__(self, parent):
		DTE.__init__(self)
		self.parent = parent
		print 'Entrando en la zona neutral. Nodo: ' + parent.ruta.estado_actual().get_nodo()
		self.localizador = gps(parent.ruta.estado_actual().get_nodo(), parent.ruta.siguiente_estado().get_orientacion())
                self.ultimo_nodo = self.localizador.get_nodo()
                
        # Devuelve la ruta precalculada
        def get_ruta(self):
                return self.parent.ruta

        # Recalcula la ruta en base a la casilla actual del robot y su orientación
        def recalcular_ruta(self, nodo, orientacion):
                ruta = self.get_ruta()
                ruta_alternativa = planificador_Aestrella(nodo, ruta.estado_final().get_nodo(), orientacion).get_ruta()
                self.parent.ruta = ruta_alternativa
	# Inputs
	def inputs(self):
		return tuple([self.localizador.get_nodo()] + list(self.parent.inputs()))

	# Estado inicial.
	def inicio(self, *args):
                self.cambiar_estado(self.interseccion)

        # Estado final.
        def fin(self, *args):
                self.localizador.close()
                self.get_ruta().avanzar()
                print 'Saliendo de la zona neutral'
                

        # Estado intersección
        def interseccion(self, *args):
                print 'Nodo actual: ' + self.get_ruta().estado_actual().get_nodo() 
                
                movimiento = self.get_ruta().siguiente_movimiento()
                if movimiento == 'left':
                        girar90('left')
                elif movimiento == 'right':
                        girar90('right')
                elif movimiento == 'forward':
                        pass
                if movimiento != 'forward':
                        # Resetear el localizador
                        self.localizador.close()
                        self.localizador = gps(self.get_ruta().estado_actual().get_nodo(), self.get_ruta().siguiente_estado().get_orientacion())
                self.cambiar_estado(self.mover)

        # Estado mover
        def mover(self, nodo_actual, ic, il, dc, dl, *args):
                if (ic == 2) and (dc == 2):
                        stop()
                else:
                        move()

                # Hemos cambiado de nodo?
                if nodo_actual != self.get_ruta().estado_actual().get_nodo():
                        print nodo_actual
                        # Avanzar a la siguiente casilla
                        self.get_ruta().avanzar()

                        # El siguiente nodo esta fuera de la zona neutral o dentro?
                        if not self.get_ruta().siguiente_estado().get_nodo() in nodos_centro:
                                self.cambiar_estado(self.ultima_interseccion)
                        else:
                                self.cambiar_estado(self.interseccion)
                                

        # Estado ultima intersección (Estamos en el último nodo de la ruta dentro de la zona
        # neutral)
        def ultima_interseccion(self, *args):
                print 'Nodo actual: ' + self.get_ruta().estado_actual().get_nodo()
                
                movimiento = self.get_ruta().siguiente_movimiento()
                if movimiento == 'left':
                        girar90('left')
                elif movimiento == 'right':
                        girar90('right')
                elif movimiento == 'forward':
                        pass

                self.cambiar_estado(self.transicion)

        # Estado mover hacia fuera (Comenzamos a movernos al siguiente nodo fuera de la zona neutral)
        def transicion(self, nodo, ic, il, dc, dl, color, *args):
                if color == 2:
                        if (dc == 2) or (dl == 2):
                                girar('left')
                        elif (ic == 2) or (il == 2):
                                girar('right')
                        else:
                                move()
                else:
                        self.cambiar_estado(self.salir)

        # Estado salir. (Nos movemos hacia fuera de la zona neutral hasta alcanzar el siguiente nodo)
        def salir(self, nodo, ic, il, dc, dl, color, *args):
                if color == 2:
                        self.cambiar_estado(self.fin)
                else:
                        if (dc == 2) or (dl == 2):
                                girar('left')
                        elif (ic == 2) or (il == 2):
                                girar('right')
                        else:
                                move()
