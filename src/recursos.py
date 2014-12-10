# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Éste módulo tiene información acerca de los directorios necesarios para
la aplicación.

"""

import os

from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import Qt

# Directorio home
HOME = os.path.expanduser("~")
# Directorio código fuente
PATH = os.path.abspath(os.path.dirname(__file__))
# Carpeta con las imágenes
PATH_ICONOS = os.path.join(PATH, "images")
# Carpeta que contiene archivos de configuración y logs
HOME_EDIS = os.path.join(HOME, ".edis")
# Archivo de configuración
CONFIGURACION = os.path.join(HOME_EDIS, "config.ini")
LOG = os.path.join(HOME_EDIS, 'edis.log')
# Selector
SELECTOR_QML = os.path.join(PATH, "ui", "selector", "selector.qml")

# Iconos
ICONOS = {}
for icono in os.listdir(PATH_ICONOS):
    ICONOS[icono.split('.')[0]] = os.path.join(PATH_ICONOS, icono)

# Atajos de teclas
ATAJOS = {
    # Archivo
    "nuevo": QKeySequence(Qt.CTRL + Qt.Key_N),
    "abrir": QKeySequence(Qt.CTRL + Qt.Key_O),
    "guardar": QKeySequence(Qt.CTRL + Qt.Key_S),
    "cerrar-tab": QKeySequence(Qt.CTRL + Qt.Key_W),
    "imprimir": QKeySequence(Qt.CTRL + Qt.Key_P),
    # Editar
    "deshacer": QKeySequence(Qt.CTRL + Qt.Key_Z),
    "rehacer": QKeySequence(Qt.CTRL + Qt.Key_Y),
    "cortar": QKeySequence(Qt.CTRL + Qt.Key_X),
    "copiar": QKeySequence(Qt.CTRL + Qt.Key_C),
    "pegar": QKeySequence(Qt.CTRL + Qt.Key_V),
    "seleccionar": QKeySequence(Qt.CTRL + Qt.Key_A),
    "indentar": QKeySequence(Qt.Key_Tab),
    "quitar-indentacion": QKeySequence(Qt.SHIFT + Qt.Key_Tab),
    "mover-arriba": QKeySequence(Qt.ALT + Qt.Key_Up),
    "mover-abajo": QKeySequence(Qt.ALT + Qt.Key_Down),
    "comentar": QKeySequence(Qt.CTRL + Qt.Key_D),
    "descomentar": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_D),
    "titulo": QKeySequence(Qt.CTRL + Qt.Key_T),
    "eliminar": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_X),
    "duplicar": QKeySequence(Qt.ALT + Qt.Key_D),
    # Ver
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "ocultar-todo": QKeySequence(Qt.Key_F11),
    "ocultar-toolbar": QKeySequence(Qt.CTRL + Qt.Key_F12),
    "ocultar-editor": QKeySequence(Qt.CTRL + Qt.Key_F1),
    "ocultar-input": QKeySequence(Qt.Key_F7),
    "zoom-mas": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "zoom-menos": QKeySequence(Qt.CTRL + Qt.Key_Minus),
    "selector": QKeySequence(Qt.CTRL + Qt.Key_M),
    # Código
    "compilar": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "ejecutar": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "comp-ejec": QKeySequence(Qt.CTRL + Qt.Key_F10),
    # Buscar
    "buscar": QKeySequence(Qt.CTRL + Qt.Key_F),
    "buscar-archivos": QKeySequence(Qt.CTRL + Qt.Key_G),
    "ir": QKeySequence(Qt.CTRL + Qt.Key_J)
    }

# Tema editor
TEMA = {
    'brace-foreground': 'red',
    'brace-background': '#b4eeb4',
    'brace-unforeground': 'white',
    'brace-unbackground': 'red',
    'margen': 'lightblue',
    'caret-background': 'gray',
    'caret-line': 'gray',
    'caret-opacidad': 40,
    'guia-fondo': 'red',
    'guia-fore': 'white',
    'sidebar-fondo': '#cecece',
    'sidebar-fore': '#acacac'
    }

# Extensiones soportadas
EXTENSIONES = " Archivos C/C++(*.cpp *.c);;ASM(*.s);;HEADERS(*.h);;(*.*)"