# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Configuraciones

"""
# Módulos Python
import sys

# Módulos QtCore
from PyQt4.QtCore import QSettings

from src import recursos

SISTEMA_OPERATIVO = sys.platform
LINUX = False
WINDOWS = False

if SISTEMA_OPERATIVO == 'win32':
    FUENTE = 'Courier'
    TAM_FUENTE = 10
    WINDOWS = True
    LINUX = False
else:
    FUENTE = 'Monospace'
    TAM_FUENTE = 12
    LINUX = True
    WINDOWS = False

MARGEN = True
MARGEN_COLUMNA = 80

INDENTACION = True
INDENTACION_ANCHO = 4
GUIAS = False

MOSTRAR_TABS = False
MODO_ENVOLVER = False

# Lateral widgets
SIMBOLOS = True
NAVEGADOR = True
EXPLORADOR = True

#FIXME: arreglar esto
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

RECIENTES = []

INICIO = True


def cargar_configuraciones():
    """ Se lee y se carga el archivo de configuracion .ini """

    qsettings = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)

    #FIXME: Evitar el uso de globals
    global MARGEN
    global MARGEN_COLUMNA
    global FUENTE
    global TAM_FUENTE
    global INDENTACION
    global INDENTACION_ANCHO
    global GUIAS
    global MOSTRAR_TABS
    global MODO_ENVOLVER
    global RECIENTES
    global INICIO
    global SIMBOLOS

    MARGEN = qsettings.value('editor/margen', True, type=bool)
    MARGEN_COLUMNA = qsettings.value('editor/margen_ancho', 80, type=int)
    fuente_f = qsettings.value('editor/fuente', "", type='QString')
    if fuente_f:
        FUENTE = fuente_f
    fuente_tam = qsettings.value('editor/tam_fuente', 0, type=int)
    if fuente_tam != 0:
        TAM_FUENTE = fuente_tam
    INDENTACION = qsettings.value('editor/indentacion', True, type=bool)
    INDENTACION_ANCHO = qsettings.value('editor/indentacion_ancho', 4, type=int)
    GUIAS = qsettings.value('editor/guias', False, type=bool)
    MOSTRAR_TABS = qsettings.value('editor/tabs', False, type=bool)
    MODO_ENVOLVER = qsettings.value('editor/envolver', False, type=bool)
    INICIO = qsettings.value('general/inicio', True, type=bool)
    RECIENTES = qsettings.value('editor/recientes', [])
    SIMBOLOS = qsettings.value('gui/simbolos', True, type=bool)