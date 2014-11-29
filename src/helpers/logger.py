# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import logging
from src import recursos


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