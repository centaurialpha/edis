# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from PyQt4.QtCore import QSettings, QSize, QPoint

from src.core import paths

# OS
IS_LINUX = True
if sys.platform.startswith('linux'):
    DEFAULT_FONT = "Monospace"
else:
    IS_LINUX = False
    DEFAULT_FONT = "Lucida Console"

# Parámetros del compilador -Wall por defecto
COMPILER_FLAGS = "-Wall"

# Braces
BRACES = {'[': ']', '(': ')'}

# Comillas
QUOTES = ["''", '""']

SETTINGS = {
    'terminal': 'xterm',
    'window/size': QSize(-1, -1),
    'window/position': QPoint(-1, -1),
    'window/show-maximized': True,
    'window/store-size': True,
    'window/style-sheet': 'Edark',
    'general/confirm-exit': True,
    'editor/complete-brace': True,
    'editor/complete-bracket': True,
    'editor/complete-paren': True,
    'editor/complete-single-quote': False,
    'editor/complete-double-quote': False,
    'editor/completion': True,
    'editor/completion-threshold': 2,
    'editor/completion-document': True,
    'editor/completion-keywords': True,
    'editor/completion-cs': False,
    'editor/completion-replace-word': False,
    'editor/completion-single': True,
    'editor/usetabs': False,
    'editor/scheme': 'dark',
    'editor/show-line-number': True,
    'editor/match-brace': True,
    'editor/mark-change': True,
    'editor/eof': False,
    'editor/show-caret-line': True,
    'editor/show-margin': True,
    'editor/width-margin': 79,
    'editor/cursor': 1,  # 0: invisilbe; 1: línea; 2: bloque
    'editor/caret-width': 1,
    'editor/cursor-period': 300,
    'editor/indent': True,
    'editor/width-indent': 4,
    'editor/show-guides': False,
    'editor/show-tabs-spaces': True,
    'editor/wrap-mode': False,
    'editor/font': "",
    'editor/size-font': 10,
    'editor/style-checker': False,
    'editor/minimap': True,
    'editor/minimap-animation': False,
    'general/language': "",
    'general/show-splash': True,
    'general/show-start-page': True,
    'general/load-files': True,
    'general/check-updates': True
    }


def load_settings():
    """ Obtiene las configuraciones desde el archivo .ini """

    settings = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
    for key, value in list(SETTINGS.items()):
        if isinstance(value, QPoint) or isinstance(value, QSize):
            _type = type(value)
        elif isinstance(value, bool):
            _type = type(value)
        elif isinstance(value, int):
            _type = type(value)
        elif isinstance(value, str):
            _type = type(value)
        if not SETTINGS['editor/font']:
            SETTINGS['editor/font'] = DEFAULT_FONT
        SETTINGS[key] = settings.value(key, defaultValue=value, type=_type)
    # Braces
    if not SETTINGS['editor/complete-paren']:
        del BRACES['(']
    if not SETTINGS['editor/complete-bracket']:
        del BRACES['[']
    # Comillas
    if not SETTINGS['editor/complete-single-quote']:
        QUOTES.remove("''")
    if not SETTINGS['editor/complete-double-quote']:
        QUOTES.remove('""')


def get_setting(key):

    """ Devuelve el valor de una configuración """

    return SETTINGS.get(key)


def set_setting(key, value):
    """ Carga un valor a SETTINGS """

    settings = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
    settings.setValue(key, value)
    SETTINGS[key] = value
