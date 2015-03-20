# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Éste módulo tiene información acerca de los directorios necesarios para
la aplicación.
"""

import sys
import os

# Home
HOME = os.path.expanduser("~")
# Código fuente
if getattr(sys, 'frozen', ''):
    # Ejecutable, cx_Freeze
    PATH = os.path.realpath(os.path.dirname(sys.argv[0]))
else:
    PATH = os.path.realpath(os.path.dirname(__file__))
EDIS = os.path.join(HOME, ".edis")
# Archivo de configuración
CONFIGURACION = os.path.join(EDIS, "edis_config.ini")
# Archivo de log
LOG = os.path.join(EDIS, "edis_log.log")


# Se crea el directorio .edis en el HOME
if not os.path.isdir(EDIS):
    os.mkdir(EDIS)
