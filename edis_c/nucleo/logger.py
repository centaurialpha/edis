# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

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

import logging
from edis_c import recursos


class Logger(object):

    __NIVELES = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critico': logging.CRITICAL
        }

    __ARCHIVO = recursos.LOG
    __FORMATO = '%(asctime)s %(levelname)s %(message)s'

    def __init__(self):
        self._hand = None
        logging.basicConfig()

    def __call__(self, nombre):
        if not self._hand:
            self.crear_handler(Logger.__ARCHIVO, 'w', Logger.__FORMATO)

        logger = logging.getLogger(nombre)
        logger.setLevel(Logger.__NIVELES['debug'])
        logger.addHandler(self._hand)
        return logger

    def crear_handler(self, archivo, modo, formato):
        fmtr = logging.Formatter(formato)
        handler = logging.FileHandler(archivo, modo)
        handler.setFormatter(fmtr)
        self._hand = handler

edisLogger = Logger()