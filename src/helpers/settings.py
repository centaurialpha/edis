# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from PyQt4.QtCore import QSettings, QSize, QPoint

from src import paths

# OS
IS_WINDOWS = False
IS_LINUX = False
if sys.platform.startswith('linux'):
    IS_LINUX = True
    DEFAULT_FONT = "Monospace"
else:
    IS_WINDOWS = True
    DEFAULT_FONT = "Consolas"

SETTINGS = {
    'window/size': QSize(-1, -1),
    'window/position': QPoint(-1, -1),
    'window/show-maximized': True,
    'window/store-size': True,
    'window/style-sheet': 'Edark',
    'general/confirm-exit': True,
    'editor/scheme': 'codeblocks',
    'editor/completion': True,
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
    'editor/style-checker': True,
    'editor/show-minimap': False,
    'general/language': "",
    'general/show-splash': True,
    'general/show-start-page': True,
    'general/load-files': True,
    'general/files': [],
    'general/recents-files': [],
    'general/check-updates': True
    }


def load_settings():
    """ Lee las configuraciones desde el archivo .ini y las carga a SETTINGS """

    settings = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
    for key, value in list(SETTINGS.items()):
        if isinstance(value, QPoint) or isinstance(value, QSize):
            _type = type(value)
        else:
            if isinstance(value, list):
                SETTINGS[key] = settings.value(key, defaultValue=value)
                continue
            else:
                _type = eval(str(type(value)).split("'")[1])
        if not SETTINGS['editor/font']:
            SETTINGS['editor/font'] = DEFAULT_FONT
        SETTINGS[key] = settings.value(key, defaultValue=value, type=_type)


def get_setting(key):
    """ Devuelve el valor de una configuración """

    return SETTINGS.get(key)


def set_setting(key, value):
    """ Carga un valor a SETTINGS """

    settings = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
    SETTINGS[key] = value
    settings.setValue(key, value)