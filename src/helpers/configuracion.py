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
if sys.platform == 'linux':
    LINUX = True
    FUENTE = 'Monospace'
    TERMINAL = ''
elif sys.platform == 'win32':
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
# configuracion[clave_QSettings] = valor_QSettings
configuracion = {
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

#FIXME:
RECIENTES = []


class ESettings(object):

    def cargar(self):
        """ Carga las configuraciones desde el archivo .ini

        QSettings.value(clave, valor, type=tipo)
        """

        qconfig = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
        configuracion['ventana/size'] = qconfig.value(
            'ventana/size', type='QSize')
        configuracion['ventana/position'] = qconfig.value(
            'ventana/position', type='QPoint')
        configuracion['general/show-start-page'] = qconfig.value(
            'general/show-start-page', True, type=bool)
        configuracion['ventana/store-size'] = qconfig.value(
            'ventana/store-size', True, type=bool)
        configuracion['general/confirm-exit'] = qconfig.value(
            'general/confirm-exit', True, type=bool)
        configuracion['editor/show-margin'] = qconfig.value(
            'editor/show-margin', True, type=bool)
        configuracion['editor/width-margin'] = qconfig.value(
            'editor/width-margin', 80, type=int)
        configuracion['editor/cursor'] = qconfig.value(
            'editor/cursor', 2, type=int)
        configuracion['editor/indent'] = qconfig.value(
            'editor/indent', True, type=bool)
        configuracion['editor/width-indent'] = qconfig.value(
            'editor/width-indent', 4, type=int)
        configuracion['editor/show-guides'] = qconfig.value(
            'editor/show-guides', False, type=bool)
        configuracion['editor/show-tabs-spaces'] = qconfig.value(
            'editor/show-tabs-spaces', False, type=bool)
        configuracion['editor/wrap-mode'] = qconfig.value(
            'editor/wrap-mode', False, type=bool)
        configuracion['editor/font'] = qconfig.value(
            'editor/font', "", type=str)
        configuracion['editor/size-font'] = qconfig.value(
            'editor/size-font', 11, type=int)
        configuracion['editor/style-checker'] = qconfig.value(
            'editor/style-checker', True, type=bool)
        configuracion['editor/show-minimap'] = qconfig.value(
            'editor/show-minimap', False, type=bool)
        configuracion['general/files'] = qconfig.value(
            'general/files', [])
        configuracion['general/recents-files'] = qconfig.value(
            'general/recents-files', [])
        configuracion['general/check-updates'] = qconfig.value(
            'general/check-updates', True, type=bool)

    @staticmethod
    def get(valor):
        return configuracion[valor]

    @staticmethod
    def set(clave, valor):
        qconfig = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
        configuracion[clave] = valor
        qconfig.setValue(clave, valor)

    @staticmethod
    def borrar():
        QSettings(paths.CONFIGURACION, QSettings.IniFormat).clear()