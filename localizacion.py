#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción: Este script define una serie de rutinas para localizar el robot
# dentro de un tablero (con forma de malla).


from matriz import matriz
from thread import start_new_thread
from threading import Condition
from time import sleep
from sensores import get_sensores_discretizados, get_dist_recorrida
from probs import *

