"""
Recursos

"""

import os
import sys

from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QColor

from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt

HOME_PATH = QDir.toNativeSeparators(QDir.homePath())

SIDE_EJEC = os.path.realpath(sys.argv[0])

PATH = os.path.abspath(os.path.dirname(__file__)).decode('utf-8')

HOME_SIDE = os.path.join(PATH, ".side_c")

CONFIGURACIONES_PATH = os.path.join(HOME_SIDE, 'side_settings.ini')

TEMA_BLACK_SIDE = os.path.join(PATH, "temas", "tema_side.qss")
TEMA_POR_DEFECTO = os.path.join(PATH, "temas", "default.qss")
TEMA_SIDE = os.path.join(PATH, "temas", "tema_por_defecto.qss")

LICENCIA = os.path.join(PATH, "../", "COPYING")

# Iconos
ICONOS = {
    "nuevo": os.path.join(PATH, "imagenes", "nuevo.png"),
    "main": os.path.join(PATH, "imagenes", "main_c.png"),
    "abrir": os.path.join(PATH, "imagenes", "abrir.png"),
    "guardar": os.path.join(PATH, "imagenes", "guardar.png"),
    "guardar-como": os.path.join(PATH, "imagenes", "guardar.png"),
    "salir": os.path.join(PATH, "imagenes", "salir.png"),
    "logo": os.path.join(PATH, "imagenes", "logo.png"),
    "icono": os.path.join(PATH, "imagenes", "side-c.png"),
    "print": os.path.join(PATH, "imagenes", "print.png"),
    "compilar": os.path.join(PATH, "imagenes", "compilar.png"),
    "ejecutar": os.path.join(PATH, "imagenes", "play.png"),
    "terminal": os.path.join(PATH, "imagenes", "terminal.png"),
    "deshacer": os.path.join(PATH, "imagenes", "deshacer.png"),
    "rehacer": os.path.join(PATH, "imagenes", "rehacer.png"),
    "cortar": os.path.join(PATH, "imagenes", "cortar.png"),
    "copiar": os.path.join(PATH, "imagenes", "copiar.png"),
    "pegar": os.path.join(PATH, "imagenes", "pegar.png"),
    "buscar": os.path.join(PATH, "imagenes", "buscar.png"),
    "icono-tab": os.path.join(PATH, "imagenes", "cambio-tab.svg"),
    "titulo": os.path.join(PATH, "imagenes", "titulo.svg"),
    "linea": os.path.join(PATH, "imagenes", "separador.png")
    }

# Estilos de color - Editor
COLOR_EDITOR = {
    "texto": "#c5c8c6",
    "fondo": "#1d1f21",
    "fondo-input": "#2d2d2d",
    "linea-actual": "#919191",
    "widget-num-linea": "#7a7a7a",
    "fondo-margen": "#cacad4",
    "opacidad": 15,
    "numero-linea": "#1d1d1d",
    "num-seleccionado": "#3c64c8",
    "margen-linea": "#777777"
    }

# Color del resaltado de sintaxis
HIGHLIGHTER = {
    "numero": QColor(248, 160, 8),
    "include": QColor(50, 130, 200),
    "palabra": QColor(131, 193, 251),
    "funcion": QColor(66, 118, 154),
    "comentario-simple": QColor(94, 205, 55),
    "comentario-multiple": QColor(105, 105, 105),
    "cadena": QColor(217, 200, 134),
    "braces": QColor(255, 255, 255)
    }

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
    # Ver
    "ocultar-menu": QKeySequence(Qt.CTRL + Qt.Key_F10),
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "modo-dev": QKeySequence(Qt.CTRL + Qt.Key_F9),
    "ocultar-toolbar": QKeySequence(Qt.CTRL + Qt.Key_F12),
    "ocultar-menu": QKeySequence(Qt.CTRL + Qt.Key_F8),
    "ocultar-input": QKeySequence(Qt.CTRL + Qt.Key_F7),
    "zoom-mas": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "zoom-menos": QKeySequence(Qt.CTRL + Qt.Key_Minus)
    }


# Extensiones soportadas
EXTENSIONES = " Archivos C (*.c *.cpp *.h)"