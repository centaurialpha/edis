# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from PyQt4.QtCore import QSettings

from src import paths


LINUX = False
WINDOWS = False

#FIXME: Mac OS
if sys.platform.startswith('linux'):
    LINUX = True
    FUENTE = 'Monospace'
    TERMINAL = ''
elif sys.platform.startswith('win'):
    WINDOWS = True
    FUENTE = 'Courier'

TOOLBAR_ITEMS = [
    "new",
    "open",
    "save",
    "separator",
    "undo",
    "redo",
    "separator",
    "copy",
    "cut",
    "paste",
    "separator",
    "build",
    "run",
    "stop"
    ]

# Configuracion por defecto
# settings[clave_QSettings] = valor_QSettings
settings = {
    'ventana/size': 0,
    'ventana/position': 0,
    'ventana/store-size': True,
    'general/confirm-exit': True,
    'editor/show-margin': True,
    'editor/width-margin': 80,
    'editor/cursor': 2,  # 0: invisilbe; 1: línea; 2: bloque
    'editor/indent': True,
    'editor/width-indent': 4,
    'editor/show-guides': False,
    'editor/show-tabs-spaces': False,
    'editor/wrap-mode': False,
    'editor/font': "",
    'editor/size-font': 10,
    'editor/style-checker': True,
    'editor/show-minimap': False,
    'general/show-start-page': True,
    'general/files': [],
    'general/recents-files': [],
    'general/check-updates': True
    }


class ESettings(object):

    def cargar(self):
        """ Carga las configuraciones desde el archivo .ini

        QSettings.value(clave, valor, type=tipo)
        """

        qconfig = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
        settings['ventana/size'] = qconfig.value(
            'ventana/size', type='QSize')
        settings['ventana/position'] = qconfig.value(
            'ventana/position', type='QPoint')
        settings['general/show-start-page'] = qconfig.value(
            'general/show-start-page', True, type=bool)
        settings['ventana/store-size'] = qconfig.value(
            'ventana/store-size', True, type=bool)
        settings['general/confirm-exit'] = qconfig.value(
            'general/confirm-exit', True, type=bool)
        settings['editor/show-margin'] = qconfig.value(
            'editor/show-margin', True, type=bool)
        settings['editor/width-margin'] = qconfig.value(
            'editor/width-margin', 80, type=int)
        settings['editor/cursor'] = qconfig.value(
            'editor/cursor', 2, type=int)
        settings['editor/indent'] = qconfig.value(
            'editor/indent', True, type=bool)
        settings['editor/width-indent'] = qconfig.value(
            'editor/width-indent', 4, type=int)
        settings['editor/show-guides'] = qconfig.value(
            'editor/show-guides', False, type=bool)
        settings['editor/show-tabs-spaces'] = qconfig.value(
            'editor/show-tabs-spaces', False, type=bool)
        settings['editor/wrap-mode'] = qconfig.value(
            'editor/wrap-mode', False, type=bool)
        settings['editor/font'] = qconfig.value(
            'editor/font', "", type=str)
        settings['editor/size-font'] = qconfig.value(
            'editor/size-font', 11, type=int)
        settings['editor/style-checker'] = qconfig.value(
            'editor/style-checker', True, type=bool)
        settings['editor/show-minimap'] = qconfig.value(
            'editor/show-minimap', False, type=bool)
        settings['general/files'] = qconfig.value(
            'general/files', [])
        settings['general/recents-files'] = qconfig.value(
            'general/recents-files', [])
        settings['general/check-updates'] = qconfig.value(
            'general/check-updates', True, type=bool)

    @staticmethod
    def get(valor):
        return settings[valor]

    @staticmethod
    def set(clave, valor):
        qconfig = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
        settings[clave] = valor
        qconfig.setValue(clave, valor)

    @staticmethod
    def clear():
        QSettings(paths.CONFIGURACION, QSettings.IniFormat).clear()