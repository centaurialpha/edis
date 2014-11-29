# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
"""
Recursos

"""
# Módulos Python
import os
import sys

# Módulos QtGui
from PyQt4.QtGui import QKeySequence

# Módulos QtCore
from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt

# Carpetas
HOME_PATH = unicode(QDir.toNativeSeparators(QDir.homePath()))
SIDE_EJEC = os.path.realpath(sys.argv[0])
PATH = os.path.abspath(os.path.dirname(__file__)).decode('utf-8')
frozen = getattr(sys, 'frozen', '')
if frozen in ('dll', 'console_exe', 'windows_exe'):
    PATH = os.path.abspath(os.path.dirname(sys.executable))

PATH_ICONOS = os.path.join(PATH, "images")
HOME_EDIS = os.path.join(HOME_PATH, ".edis")
CONFIGURACION = os.path.join(HOME_EDIS, "config.ini")
OTROS = (HOME_EDIS, 'otros')
LOG = os.path.join(HOME_EDIS, 'edis.log')
INSTALADOR = os.path.join(PATH, "nucleo", "mingw.exe")
IDIOMAS = os.path.join(HOME_EDIS, "otros", "idiomas")
TEMA_POR_DEFECTO = os.path.join(PATH, "otros", "temas", "default.qss")
TEMAS_GUARDADOS = os.path.join(PATH, "otros", "temas", "editor")
LICENCIA = os.path.join(PATH, "../", "COPYING")
PAGINA_INICIO = os.path.join(PATH, "otros", "pagina_de_bienvenida")
NOTIFICACION = os.path.join(PATH, "otros", "QtQML")


# Iconos
ICONOS = {}
for icono in os.listdir(PATH_ICONOS):
    ICONOS[icono.split('.')[0]] = os.path.join(PATH_ICONOS, icono)


# Estilos de color - Editor
TEMA_EDITOR = {
    "texto-editor": "000000",
    "fondo-editor": "#f6f6f6",
    "fondo-seleccion-editor": "#111111",
    "seleccion-editor": "#5acd14",
    "salida-exitosa": "#5acd14",
    "salida-error": "red",
    "fondo-input": "#1e1e1e",
    "linea-actual": "red",
    "widget-num-linea": "#cecece",
    "fondo-margen": "#232323",
    "opacidad": 15,
    "numero-linea": "#acacac",
    "num-seleccionado": "#bfbfbf",
    "margen-linea": "lightblue",
    "palabra": "darkblue",
    "operador": "black",
    "types": "darkblue",
    "brace": "black",
    "struct": "gray",
    "cadena": "red",
    "caracter": "red",
    "include": "#228b22",
    "comentario": "gray",
    "numero": "#F8A032",
    "pcoma": "black"
    }

NUEVO_TEMA = {}

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
    # Código
    "compilar": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "ejecutar": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "comp-ejec": QKeySequence(Qt.CTRL + Qt.Key_F10),
    # Buscar
    "buscar": QKeySequence(Qt.CTRL + Qt.Key_F),
    "buscar-archivos": QKeySequence(Qt.CTRL + Qt.Key_G),
    "ir": QKeySequence(Qt.CTRL + Qt.Key_J)
    }

# Extensiones soportadas
EXTENSIONES = " Archivos C/C++(*.cpp *.c);;ASM(*.s);;HEADERS(*.h);;(*.*)"
