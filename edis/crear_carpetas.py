# -*- coding: utf-8 -*-

# This file is part of EDIS.

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

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