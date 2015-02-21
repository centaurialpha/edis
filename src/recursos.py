# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import Qt


# Atajos
SHORTCUTS = {
    # Archivo
    "new": QKeySequence(Qt.CTRL + Qt.Key_N),
    "open": QKeySequence(Qt.CTRL + Qt.Key_O),
    "save": QKeySequence(Qt.CTRL + Qt.Key_S),
    "close": QKeySequence(Qt.CTRL + Qt.Key_W),
    "properties": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P),
    "exit": QKeySequence(Qt.CTRL + Qt.Key_Q),
    # Editar
    "undo": QKeySequence(Qt.CTRL + Qt.Key_Z),
    "redo": QKeySequence(Qt.CTRL + Qt.Key_Y),
    "cut": QKeySequence(Qt.CTRL + Qt.Key_X),
    "copy": QKeySequence(Qt.CTRL + Qt.Key_C),
    "paste": QKeySequence(Qt.CTRL + Qt.Key_V),
    "select": QKeySequence(Qt.CTRL + Qt.Key_A),
    "indent": QKeySequence(Qt.Key_Tab),
    "unindent": QKeySequence(Qt.SHIFT + Qt.Key_Tab),
    "up": QKeySequence(Qt.ALT + Qt.Key_Up),
    "down": QKeySequence(Qt.ALT + Qt.Key_Down),
    "comment": QKeySequence(Qt.CTRL + Qt.Key_D),
    "uncomment": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_D),
    "title": QKeySequence(Qt.CTRL + Qt.Key_T),
    "delete": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_X),
    "duplicate": QKeySequence(Qt.ALT + Qt.Key_D),
    "preferences": QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_P),
    # Ver
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "hide-all": QKeySequence(Qt.Key_F11),
    "hide-toolbar": QKeySequence(Qt.Key_F8),
    "hide-output": QKeySequence(Qt.Key_F7),
    "zoom-in": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "zoom-out": QKeySequence(Qt.CTRL + Qt.Key_Minus),
    "show-selector": QKeySequence(Qt.CTRL + Qt.Key_M),
    # Código
    "build": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "run": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "build-run": QKeySequence(Qt.CTRL + Qt.Key_F10),
    "stop": QKeySequence(Qt.CTRL + Qt.Key_B),
    # Buscar
    "find": QKeySequence(Qt.CTRL + Qt.Key_F),
    "find-replace": QKeySequence(Qt.CTRL + Qt.Key_H),
    "go-to-line": QKeySequence(Qt.CTRL + Qt.Key_J)
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