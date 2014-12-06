# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

#from PyQt4.QtGui import (
    #QMenuBar

from PyQt4.QtCore import (
    QObject
    )

from src.ui.edis_main import EDIS

NUEVO = {
    'nombre': 'Nuevo',
    'atajo': 'Ctrl+N',
    'icono': None,
    'connect': None
    }

ABRIR = {
    'nombre': 'Abrir',
    'atajo': 'Ctrl+O',
    'icono': None,
    'connect': None
    }

DESHACER = {
    'nombre': 'Deshacer',
    'atajo': 'Ctrl+Z',
    'icono': None,
    'connect': None
    }

REHACER = {
    'nombre': 'Rehacer',
    'atajo': 'Ctrl+Y',
    'icono': None,
    'connect': None
    }

ITEMS = {
    0: (NUEVO, ABRIR),
    1: (DESHACER, REHACER)
    }


class Menu(QObject):

    def __init__(self):
        super(Menu, self).__init__()

        EDIS.cargar_componente("menu", self)

    def cargar_menu(self, edis):
        menu = edis.menuBar()
        for i in range(2):
            root = menu.addMenu(edis.get_menu(i))
            for e in ITEMS[i]:
                accion = root.addAction(e['nombre'])
                atajo = e['atajo']
                accion.setShortcut(atajo)
                root.addAction(accion)
            #pass


menu = Menu()