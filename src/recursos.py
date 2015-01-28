# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Éste módulo tiene información acerca de los directorios necesarios para
la aplicación.

"""

from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import Qt


# Atajos de teclas
ATAJOS = {
    # Archivo
    "nuevo": QKeySequence(Qt.CTRL + Qt.Key_N),
    "abrir": QKeySequence(Qt.CTRL + Qt.Key_O),
    "guardar": QKeySequence(Qt.CTRL + Qt.Key_S),
    "cerrar-tab": QKeySequence(Qt.CTRL + Qt.Key_W),
    "imprimir": QKeySequence(Qt.CTRL + Qt.Key_P),
    "propiedades": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P),
    "salir": QKeySequence(Qt.CTRL + Qt.Key_Q),
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
    "preferencias": QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_P),
    # Ver
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "ocultar-todo": QKeySequence(Qt.Key_F11),
    "mostrar-toolbar": QKeySequence(Qt.Key_F8),
    "lateral": QKeySequence(Qt.Key_F6),
    "mostrar-compilador": QKeySequence(Qt.Key_F7),
    "acercar": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "alejar": QKeySequence(Qt.CTRL + Qt.Key_Minus),
    "selector": QKeySequence(Qt.CTRL + Qt.Key_M),
    # Código
    "compilar": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "ejecutar": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "comp-ejec": QKeySequence(Qt.CTRL + Qt.Key_F10),
    # Buscar
    "busqueda-rapida": QKeySequence(Qt.CTRL + Qt.Key_F),
    "buscar": QKeySequence(Qt.CTRL + Qt.Key_H),
    "ir": QKeySequence(Qt.CTRL + Qt.Key_J)
    }

# Tema editor
TEMA = {
    'FondoEditor': '#121212',
    'Color': '#c2c2c2',
    'Keyword': '#87afd7',
    'KeywordSet2': '#87afd7',
    'Comment': '#af5f5f',
    'CommentLine': '#af5f5f',
    'Number': '#d7d75f',
    'DoubleQuotedString': '#5e7366',
    'SingleQuotedString': '#5e7366',
    'PreProcessor': '#87afd7',
    'PreProcessorComment': 'orange',
    'Operator': 'white',
    'RawString': 'orange',
    'UUID': 'orange',
    'HashQuotedString ': 'blue',
    'brace-foreground': 'white',
    'brace-background': '#044888',
    'brace-unforeground': 'white',
    'brace-unbackground': 'red',
    'margen': '#4d4d4d',
    'caret-background': 'gray',
    'caret-line': '#687073',
    'caret-opacidad': 20,
    'guia-fondo': 'red',
    'guia-fore': 'white',
    'sidebar-fondo': '#212121',
    'sidebar-fore': '#85878c',
    'foldFore': '#242424',
    'foldBack': '#242424',
    'error': '#e73e3e'
    }