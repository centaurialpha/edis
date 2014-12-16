# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Configuraciones

"""
# Módulos Python
import sys

# Módulos QtCore
from PyQt4.QtCore import QSettings

from src import recursos

###############################################################################
#                        MÁRGEN                                               #
###############################################################################
MARGEN = True
MARGEN_COLUMNA = 80
###############################################################################
#                   SISTEMA OPERATIVO                                         #
###############################################################################
SISTEMA_OPERATIVO = sys.platform

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

###############################################################################
# FUENTE
###############################################################################
FUENTE_MAX_TAM = 80
FUENTE_MIN_TAM = 6

###############################################################################
# INDENTACION
###############################################################################
INDENTACION = 4
CHECK_INDENTACION = True
CHECK_AUTOINDENTACION = True
GUIA_INDENTACION = False
###############################################################################
# TABS Y ESPACIOS
###############################################################################
MOSTRAR_TABS = False
MODO_ENVOLVER = False
###############################################################################
# MINIMAPA
###############################################################################
MINIMAPA = False
MINI_TAM = 0.17
OPAC_MIN = 0.2
OPAC_MAX = 0.9
MAX_RECIENTES = 5
SIDEBAR = True

CONFIRMAR_AL_CERRAR = True
IDIOMAS = []
IDIOMA = ""
PARAMETROS = ""
TERMINAL = ""

# Lateral widgets
SYMBOLS = True
FILE_EXPLORER = True
FILE_NAVIGATOR = True

ITEMS_TOOLBAR = [
    'Nuevo',
    'Abrir'
    ]

COMILLAS = {
    "'": "'",  # Comillas simples
    '"': '"'  # Comillas dobles
    }

BRACES = {
    '{': '}',
    '[': ']',
    '(': ')'
    }


###############################################################################
def cargar_configuraciones():
    """ Se lee y se carga el archivo de configuracion .ini """

    qsettings = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)

    global MARGEN
    global MARGEN_COLUMNA
    global FUENTE
    global TAM_FUENTE
    global INDENTACION
    global GUIA_INDENTACION
    global CHECK_INDENTACION
    global CHECK_AUTOINDENTACION
    global MOSTRAR_TABS
    global MODO_ENVOLVER
    global SIDEBAR
    global MINIMAPA
    global MINI_TAM
    global OPAC_MIN
    global OPAC_MAX
    global CONFIRMAR_AL_CERRAR
    global IDIOMA
    global PARAMETROS
    global TERMINAL
    MARGEN_COLUMNA = qsettings.value('configuraciones/editor/margenLinea', 80,
                             type=int)
    MARGEN = qsettings.value(
        'configuraciones/editor/mostrarMargen', True, type=bool)
    fuente_f = qsettings.value(
        'configuraciones/editor/fuente', "", type='QString')
    if fuente_f:
        FUENTE = fuente_f
    fuente_tam = qsettings.value(
        'configuraciones/editor/fuenteTam', 0, type=int)
    if fuente_tam != 0:
        TAM_FUENTE = fuente_tam
    INDENTACION = int(qsettings.value('configuraciones/editor/indentacion',
                                      4, type=int))
    GUIA_INDENTACION = qsettings.value('configuraciones/editor/guiaInd',
                                       False, type=bool)
    CHECK_INDENTACION = qsettings.value('configuraciones/editor/checkInd',
                                        True, type=bool)
    CHECK_AUTOINDENTACION = qsettings.value('configuraciones/editor/autoInd',
                                            True, type=bool)
    MOSTRAR_TABS = qsettings.value(
        'configuraciones/editor/tabs', False, type=bool)
    MODO_ENVOLVER = qsettings.value('configuraciones/editor/envolver',
                                    False, type=bool)
    SIDEBAR = qsettings.value('configuraciones/editor/sidebar', True,
                              type=bool)
    MINIMAPA = qsettings.value('configuraciones/editor/mini', True, type=bool)
    MINI_TAM = float(qsettings.value('configuraciones/editor(miniTam',
                                     0.17, type=float))
    OPAC_MIN = float(qsettings.value('configuraciones/editor/opac_min',
                                     0.2, type=float))
    OPAC_MAX = float(qsettings.value('configuraciones/editor/opac_max',
                                     0.9, type=float))
    TERMINAL = qsettings.value('configuraciones/ejecucion/terminal', "",
        type='QString')
    CONFIRMAR_AL_CERRAR = qsettings.value(
        'configuraciones/general/confirmacionCerrar', True).toBool()
    IDIOMA = qsettings.value('configuraciones/general/idioma',
                             '', type='QString')
    PARAMETROS = qsettings.value('configuraciones/compilacion',
                                 defaultValue='', type='QString')
    comillas_simples = qsettings.value('configuraciones/editor/comillasS',
                                       True, type=bool)

    if not comillas_simples:
        del COMILLAS["'"]
    comillas_dobles = qsettings.value('configuraciones/editor/comillasD',
                                      True).toBool()
    if not comillas_dobles:
        del COMILLAS['"']
    llaves = qsettings.value('configuraciones/editor/llaves',
                             True).toBool()
    if not llaves:
        del BRACES['{']
    corchetes = qsettings.value('configuraciones/editor/corchetes',
                                True).toBool()
    if not corchetes:
        del BRACES['[']
    parentesis = qsettings.value('configuraciones/editor/parentesis',
                                 True).toBool()
    if not parentesis:
        del BRACES['(']
