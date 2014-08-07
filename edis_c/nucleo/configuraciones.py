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
# Módulos Python
import sys

# Módulos QtCore
from PyQt4.QtCore import QSettings

#from edis_c import recursos

###############################################################################
#                        MÁRGEN                                               #
###############################################################################
MARGEN = 80
MOSTRAR_MARGEN = False
OPACIDAD_MARGEN = 17
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
GUIA_INDENTACION = False
###############################################################################
# TABS Y ESPACIOS
###############################################################################
MOSTRAR_TABS = True
MODO_ENVOLVER = False
###############################################################################
# MINIMAPA
###############################################################################
MINIMAPA = True
MINI_TAM = 0.17
OPAC_MIN = 0.2
OPAC_MAX = 0.9
POSS = 0
SIDEBAR = True

PAGINA_BIENVENIDA = True
CONFIRMAR_AL_CERRAR = True
IDIOMAS = []
IDIOMA = ""
ULTIMA_SESION = True
PARAMETROS = ""

BARRA_HERRAMIENTAS_ITEMS = [
    "separador",
    "nuevo-archivo",
    "abrir-archivo",
    "guardar-archivo",
    "separador",
    "deshacer",
    "rehacer",
    "cortar",
    "copiar",
    "pegar",
    "separador",
    "indentar",
    "desindentar",
    "include",
    "titulo",
    "linea",
    "separador",
    "compilar-archivo",
    "ejecutar-archivo",
    "compilar-ejecutar-archivo",
    "separador"
    #"frenar",
    ]

BARRA_HERRAMIENTAS_ORIGINAL = [
    "separador",
    "nuevo-archivo",
    "abrir-archivo",
    "guardar-archivo",
    "separador",
    "deshacer",
    "rehacer",
    "cortar",
    "copiar",
    "pegar",
    "separador",
    "indentar",
    "desindentar",
    "include",
    "titulo",
    "linea",
    "separador",
    "compilar-archivo",
    "ejecutar-archivo",
    "compilar-ejecutar-archivo",
    "separador"
    #"frenar",
    ]


###############################################################################
def cargar_configuraciones():
    qsettings = QSettings()
    global MARGEN
    global MOSTRAR_MARGEN
    global OPACIDAD_MARGEN
    global FUENTE
    global TAM_FUENTE
    global INDENTACION
    global GUIA_INDENTACION
    global CHECK_INDENTACION
    global CHECK_AUTO_INDENTACION
    global MOSTRAR_TABS
    global MINIMAPA
    global MINI_TAM
    global OPAC_MIN
    global OPAC_MAX
    global PAGINA_BIENVENIDA
    global CONFIRMAR_AL_CERRAR
    global IDIOMA
    global PARAMETROS
    global BARRA_HERRAMIENTAS_ITEMS
    global ULTIMA_SESION
    MARGEN = qsettings.value('configuraciones/editor/margenLinea', 80, type=int)
    MOSTRAR_MARGEN = qsettings.value(
        'configuraciones/editor/mostrarMargen', False, type=bool)
    OPACIDAD_MARGEN = int(qsettings.value(
        'configuraciones/editor/opacidadMargen', 15, type=int))
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
    CHECK_INDENTACION = qsettings.value('configuraciones/editor/checkInd', True,
        type=bool)
    CHECK_AUTO_INDENTACION = qsettings.value('configuraciones/editor/autoInd',
        True, type=bool)
    MOSTRAR_TABS = qsettings.value(
        'configuraciones/editor/tabs', True, type=bool)
    MINIMAPA = qsettings.value('configuraciones/editor/mini', True, type=bool)
    MINI_TAM = float(qsettings.value('configuraciones/editor(miniTam',
    0.17, type=float))
    OPAC_MIN = float(qsettings.value('configuraciones/editor/opac_min',
        0.2, type=float))
    OPAC_MAX = float(qsettings.value('configuraciones/editor/opac_max',
        0.9, type=float))
    PAGINA_BIENVENIDA = qsettings.value(
        'configuraciones/general/paginaBienvenida', True).toBool()
    CONFIRMAR_AL_CERRAR = qsettings.value(
        'configuraciones/general/confirmacionCerrar', True).toBool()
    IDIOMA = qsettings.value('configuraciones/general/idioma',
        '', type='QString')
    PARAMETROS = qsettings.value('configuraciones/compilacion',
        defaultValue='', type='QString')
    items_barra = [str(i.toString()) for i in qsettings.value(
        'configuraciones/gui/barra', []).toList()]
    if items_barra:
        BARRA_HERRAMIENTAS_ITEMS = items_barra
    ULTIMA_SESION = qsettings.value('configuraciones/general/ultimaSesion',
        True, type=bool)