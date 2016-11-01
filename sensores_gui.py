#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# Descripción:
# Módulo que muestra los valores de los sensores actualmente en una interfaz
# de usuario.

import curses;
from time import sleep
from sensores import get_sensores, discretizar

std = curses.initscr()
curses.noecho()
curses.cbreak()
std.keypad(1)

try:
	while True:
		ic, il, dc, dl = get_sensores()
		dic, dil, ddc, ddl = discretizar(*get_sensores())
		
		std.addstr(0, 0, "Sensor izquierdo central: " + repr(ic))
		std.addstr(1, 0, "Sensor izquierdo lateral: " + repr(il))
		std.addstr(2, 0, "Sensor derecho central:   " + repr(dc))
		std.addstr(3, 0, "Sensor derecho lateral:   " + repr(dl))
		std.refresh()
		sleep(.5)
except KeyboardInterrupt:
	pass
finally:
	curses.nocbreak(); 
	std.keypad(0); 
	curses.echo()
	curses.endwin()

	
