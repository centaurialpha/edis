# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from . import recursos


def crear_carpetas_edis():
    """ Se crea la estructura de carpetas que guarda archivos de
        configuracion, temas, etc.
    """

    if not es_carpeta(recursos.HOME_EDIS):
        os.mkdir(recursos.HOME_EDIS)


def es_carpeta(carpeta):
    if os.path.isdir(carpeta):
        return True
    return False