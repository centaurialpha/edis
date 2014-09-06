# -*- coding: utf-8 -*-

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

from edis_c import recursos

###############################################################################
#                        MÁRGEN                                               #
###############################################################################
MARGEN = 80
MOSTRAR_MARGEN = True
OPACIDAD_MARGEN = 0
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
CHECK_AUTOINDENTACION = True
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
MAX_RECIENTES = 5
SIDEBAR = True

PAGINA_BIENVENIDA = True
CONFIRMAR_AL_CERRAR = True
IDIOMAS = []
IDIOMA = ""
#ULTIMA_SESION = True
PARAMETROS = ""

BARRA_HERRAMIENTAS_ITEMS = [
    "separador",
    "nuevo-archivo",
    "abrir-archivo",
    "guardar-archivo",
    "guardar-como",
    "guardar-todo",
    "separador",
    "deshacer",
    "rehacer",
    "cortar",
    "copiar",
    "pegar",
    "buscar",
    "separador",
    "acercar",
    "alejar",
    "separador",
    "indentar",
    "desindentar",
    "arriba",
    "abajo",
    "include",
    "macro",
    "linea",
    "separador",
    "compilar-archivo",
    "ejecutar-archivo",
    "compilar-ejecutar-archivo",
    "frenar",
    "separador"
    ]

BARRA_HERRAMIENTAS_ORIGINAL = [
    "separador",
    "nuevo-archivo",
    "abrir-archivo",
    "guardar-archivo",
    "guardar-como",
    "guardar-todo",
    "separador",
    "deshacer",
    "rehacer",
    "cortar",
    "copiar",
    "pegar",
    "buscar",
    "separador",
    "acercar",
    "alejar",
    "separador",
    "indentar",
    "desindentar",
    "arriba",
    "abajo",
    "include",
    "macro",
    "linea",
    "separador",
    "compilar-archivo",
    "ejecutar-archivo",
    "compilar-ejecutar-archivo",
    "frenar",
    "separador"
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
    global MOSTRAR_MARGEN
    global OPACIDAD_MARGEN
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
    global PAGINA_BIENVENIDA
    global CONFIRMAR_AL_CERRAR
    global IDIOMA
    global PARAMETROS
    global BARRA_HERRAMIENTAS_ITEMS
    #global ULTIMA_SESION
    MARGEN = qsettings.value('configuraciones/editor/margenLinea', 80,
                             type=int)
    MOSTRAR_MARGEN = qsettings.value(
        'configuraciones/editor/mostrarMargen', True, type=bool)
    OPACIDAD_MARGEN = int(qsettings.value(
        'configuraciones/editor/opacidadMargen', 0, type=int))
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
        'configuraciones/editor/tabs', True, type=bool)
    MODO_ENVOLVER = qsettings.value('configuraciones/editor/envolver',
                                    True, type=bool)
    SIDEBAR = qsettings.value('configuraciones/editor/sidebar', True,
                              type=bool)
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
