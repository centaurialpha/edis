# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
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
    TAM_FUENTE = 12
    TERMINAL = ''
elif sys.platform == 'win32':
    WINDOWS = True
    FUENTE = 'Courier'
    TAM_FUENTE = 10

ITEMS_TOOLBAR = [
    'Nuevo archivo',
    'Abrir',
    'Guardar',
    'separador',
    'Deshacer',
    'separador',
    'Rehacer',
    'separador',
    'Indentar',
    'Remover indentación',
    'Compilar',
    'Ejecutar',
    'Terminar',
    'separador'
    ]

# Configuracion por defecto
# configuracion[clave_QSettings] = valor_QSettings
configuracion = {
    'ventana/dimensiones': 0,
    'ventana/posicion': 0,
    'ventana/guardarDimensiones': True,
    'general/confirmarSalida': True,
    'gui/simbolos': True,
    'gui/explorador': True,
    'gui/navegador': True,
    'editor/margen': True,
    'editor/tipoCursor': 2,  # 0: invisilbe; 1: línea; 2: bloque
    'editor/margenAncho': 80,
    'editor/indentacion': True,
    'editor/indentacionAncho': 4,
    'editor/guias': False,
    'editor/mostrarTabs': False,
    'editor/modoWrap': False,
    'editor/fuente': "",
    'editor/fuenteTam': 0,
    'general/inicio': True,
    'terminal': ''
    }

#FIXME:
RECIENTES = []


class ESettings(object):

    def cargar(self):
        """ Carga las configuraciones desde el archivo .ini

        QSettings.value(clave, valor, type=tipo)
        """

        qconfig = QSettings(paths.CONFIGURACION, QSettings.IniFormat)
        for clave, valor in list(configuracion.items()):
            tipo = eval(str(type(valor)).split("'")[1])
            if tipo == str:
                tipo = 'QString'
            elif clave == 'ventana/dimensiones':
                configuracion[clave] = qconfig.value(clave, valor)
            elif clave == 'ventana/posicion':
                configuracion[clave] = qconfig.value(clave, valor)
            else:
                configuracion[clave] = qconfig.value(clave, valor, type=tipo)
        if not configuracion['editor/fuente']:
            configuracion['editor/fuente'] = FUENTE

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