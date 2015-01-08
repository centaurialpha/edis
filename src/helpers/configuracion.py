# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from PyQt4.QtCore import QSettings

from src import recursos


LINUX = False
WINDOWS = False

#FIXME: Mac OS
if sys.platform == 'linux':
    LINUX = True
    FUENTE = 'Monospace'
    TAM_FUENTE = 12
elif sys.platform == 'win32':
    WINDOWS = True
    FUENTE = 'Currier'
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
    'gui/simbolos': True,
    'gui/explorador': True,
    'gui/navegador': True,
    'editor/margen': True,
    'editor/margenAncho': 80,
    'editor/indentacion': True,
    'editor/indentacionAncho': 4,
    'editor/guias': True,
    'editor/mostrarTabs': False,
    'editor/modoWrap': False,
    'general/inicio': True,
    }

#FIXME:
RECIENTES = []


class ESettings(object):

    def cargar(self):
        """ Carga las configuraciones desde el archivo .ini

        QSettings.value(clave, valor, type=tipo)
        """

        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        for clave, valor in list(configuracion.items()):
            configuracion[clave] = qconfig.value(clave, valor,
                type=eval(str(type(valor)).split("'")[1]))

    @staticmethod
    def get(valor):
        return configuracion[valor]

    @staticmethod
    def set(clave, valor):
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        configuracion[clave] = valor
        qconfig.setValue(clave, valor)