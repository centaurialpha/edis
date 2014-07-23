#-*- coding: utf-8 -*-

# <Directorios y otros recursos que usa el programa .>
# This file is part of EDIS-C.

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

"""
Recursos

"""

import os
import sys

from PyQt4.QtGui import QKeySequence
#from PyQt4.QtGui import QColor

from PyQt4.QtCore import QDir
from PyQt4.QtCore import Qt

HOME_PATH = QDir.toNativeSeparators(QDir.homePath())

SIDE_EJEC = os.path.realpath(sys.argv[0])

PATH = os.path.abspath(os.path.dirname(__file__)).decode('utf-8')

HOME_SIDE = os.path.join(PATH, ".edis_c")

CONFIGURACIONES_PATH = os.path.join(HOME_SIDE, 'edis_settings.ini')

IDIOMAS = os.path.join(PATH, "idiomas")
TEMA_BLACK_SIDE = os.path.join(PATH, "temas", "tema_side.qss")
TEMA_POR_DEFECTO = os.path.join(PATH, "temas", "default.qss")
TEMA_SIDE = os.path.join(PATH, "temas", "tema_por_defecto.qss")
TEMAS_GUARDADOS = os.path.join(PATH, "temas", "editor")
LICENCIA = os.path.join(PATH, "../", "COPYING")

PAGINA_INICIO = os.path.join(PATH, "pagina_inicio")

# Iconos
ICONOS = {
    "nuevo": os.path.join(PATH, "imagenes", "nuevo.png"),
    "main": os.path.join(PATH, "imagenes", "main_c.png"),
    "abrir": os.path.join(PATH, "imagenes", "abrir.png"),
    "guardar": os.path.join(PATH, "imagenes", "guardar.png"),
    "guardar-como": os.path.join(PATH, "imagenes", "guardar.png"),
    "salir": os.path.join(PATH, "imagenes", "salir.png"),
    "splash": os.path.join(PATH, "imagenes", "splash.png"),
    "icono": os.path.join(PATH, "imagenes", "side-c.png"),
    # Logo dragón (originalmente verde by nessmasta) - modificado a azul
    "seiryu": os.path.join(PATH, "imagenes", "edis_seiryu.png"),
    "seiryu_icono": os.path.join(PATH, "imagenes", "seiryu_icono.png"),
    "print": os.path.join(PATH, "imagenes", "print.png"),
    "compilar": os.path.join(PATH, "imagenes", "compilar.png"),
    "ejecutar": os.path.join(PATH, "imagenes", "play.png"),
    "comp-ejec": os.path.join(PATH, "imagenes", "compilar-ejecutar.png"),
    "frenar": os.path.join(PATH, "imagenes", "frenar.png"),
    "terminal": os.path.join(PATH, "imagenes", "terminal.png"),
    "notas": os.path.join(PATH, "imagenes", "notas.png"),
    "deshacer": os.path.join(PATH, "imagenes", "deshacer.png"),
    "rehacer": os.path.join(PATH, "imagenes", "rehacer.png"),
    "cortar": os.path.join(PATH, "imagenes", "cortar.png"),
    "copiar": os.path.join(PATH, "imagenes", "copiar.png"),
    "pegar": os.path.join(PATH, "imagenes", "pegar.png"),
    "buscar": os.path.join(PATH, "imagenes", "buscar.png"),
    "icono-tab": os.path.join(PATH, "imagenes", "cambio-tab.svg"),
    "titulo": os.path.join(PATH, "imagenes", "titulo.svg"),
    "linea": os.path.join(PATH, "imagenes", "separador.png"),
    "general": os.path.join(PATH, "imagenes", "general.png"),
    "editor": os.path.join(PATH, "imagenes", "editor.png"),
    "tema": os.path.join(PATH, "imagenes", "tema.png"),
    "indentar": os.path.join(PATH, "imagenes", "indentar.png"),
    "desindentar": os.path.join(PATH, "imagenes", "desindentar.png"),
    "comentar": os.path.join(PATH, "imagenes", "comentar.png"),
    "insertar-include": os.path.join(PATH, "imagenes", "insertar-include.png")
    }

# Estilos de color - Editor
TEMA_EDITOR = {
    "texto-editor": "#666",
    "fondo-editor": "#ffffff",
    "fondo-seleccion-editor": "#111111",
    "seleccion-editor": "#5acd14",
    "salida-exitosa": "#5acd14",
    "salida-error": "red",
    "fondo-input": "#1e1e1e",
    "linea-actual": "#919191",
    "widget-num-linea": "#7a7a7a",
    "fondo-margen": "#cacad4",
    "opacidad": 15,
    "numero-linea": "#1d1d1d",
    "num-seleccionado": "#3c64c8",
    "margen-linea": "#777777",
    #"include_": QColor(155, 207, 217),
    #"palabra": QColor(138, 226, 52),
    "palabra": "#96BE0A",
    "operador": "yellow",
    "brace": "#1E1E1E",
    "struct": "black",
    "cadena": "#640AE1",
    "caracter": "blue",
    "include": "#3282C8",
    "comentario": "#E10A1E",
    "numero": "#F8A032"
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
    "mover-arriba": QKeySequence(Qt.ALT + Qt.Key_Up),
    "mover-abajo": QKeySequence(Qt.ALT + Qt.Key_Down),
    # Ver
    "ocultar-menu": QKeySequence(Qt.CTRL + Qt.Key_F10),
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "modo-dev": QKeySequence(Qt.CTRL + Qt.Key_F9),
    "ocultar-toolbar": QKeySequence(Qt.CTRL + Qt.Key_F12),
    "ocultar-lateral": QKeySequence(Qt.Key_F10),
    "ocultar-menu": QKeySequence(Qt.CTRL + Qt.Key_F8),
    "ocultar-input": QKeySequence(Qt.Key_F7),
    "zoom-mas": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "zoom-menos": QKeySequence(Qt.CTRL + Qt.Key_Minus),
    # Código
    "compilar": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "ejecutar": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "comp-ejec": QKeySequence(Qt.CTRL + Qt.Key_F10),
    # Buscar
    "buscar": QKeySequence(Qt.CTRL + Qt.Key_F)
    }


# Extensiones soportadas
EXTENSIONES = " Archivos C (*.c *.s *.h)"