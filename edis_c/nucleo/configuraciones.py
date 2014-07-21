#-*- coding: utf-8 -*-

# <Configuraciones.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

"""
Configuraciones

"""
import sys

from PyQt4.QtCore import QSettings

from edis_c import recursos

###############################################################################
#                        MÁRGEN                                               #
###############################################################################
MARGEN = 80
MOSTRAR_MARGEN = False

###############################################################################
#                   SISTEMA OPERATIVO                                         #
###############################################################################
SISTEMA_OPERATIVO = sys.platform
WIN = 'win32'
TUX = 'linux2'

if SISTEMA_OPERATIVO == WIN:
    FUENTE = 'Courier'
    TAM_FUENTE = 10
    WINDOWS = True
    LINUX = False
else:
    try:
        FUENTE = 'Ubuntu Mono'
        TAM_FUENTE = 12
        LINUX = True
        WINDOWS = False
    except:
        FUENTE = 'Monospace'
        TAM_FUENTE = 11
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
CHECK_AUTO_INDENTACION = True

###############################################################################
# TABS Y ESPACIOS
###############################################################################
MOSTRAR_TABS = True
MODO_ENVOLVER = False
###############################################################################
# MINIMAPA
###############################################################################
MINIMAPA = True
OPAC_MIN = 0.2
OPAC_MAX = 0.9

SIDEBAR = True

MOSTRAR_PAGINA_INICIO = True

IDIOMAS = []
IDIOMA = ""

PARAMETROS = ""


###############################################################################
def cargar_configuraciones():
    global MARGEN
    global MOSTRAR_MARGEN
    global FUENTE
    global TAM_FUENTE
    global INDENTACION
    global CHECK_INDENTACION
    global CHECK_AUTO_INDENTACION
    global MOSTRAR_TABS
    global MINIMAPA
    global OPAC_MIN
    global OPAC_MAX
    global MOSTRAR_PAGINA_INICIO
    global IDIOMA
    global PARAMETROS

    qsettings = QSettings(recursos.CONFIGURACIONES_PATH, QSettings.IniFormat)

    MARGEN = qsettings.value('configuraciones/editor/margenLinea', 80, type=int)
    MOSTRAR_MARGEN = qsettings.value(
        'configuraciones/editor/mostrarMargen', False, type=bool)
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
    CHECK_INDENTACION = qsettings.value('configuraciones/editor/checkInd', True,
        type=bool)
    CHECK_AUTO_INDENTACION = qsettings.value('configuraciones/editor/autoInd',
        True, type=bool)
    MOSTRAR_TABS = qsettings.value(
        'configuraciones/editor/tabs', True, type=bool)
    MINIMAPA = qsettings.value('configuraciones/editor/mini', True, type=bool)
    OPAC_MIN = float(qsettings.value('configuraciones/editor/opac_min',
        0.2, type=float))
    OPAC_MAX = float(qsettings.value('configuraciones/editor/opac_max',
        0.9, type=float))
    MOSTRAR_PAGINA_INICIO = qsettings.value(
        'configuraciones/general/paginaInicio', True, type=bool)
    IDIOMA = qsettings.value('configuraciones/general/idioma',
        '', type='QString')
    PARAMETROS = qsettings.value('configuraciones/compilacion',
        defaultValue='', type='QString')