# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Logger """

import logging
from src.core import paths

# Fecha Hora   Módulo:Función:Línea   Nivel Mensaje
FORMAT = "%(asctime)s %(name)10s:%(funcName)s:%(lineno)s " \
              "%(levelname)10s %(message)10s"
FORMAT_TIME = "%y-%m-%d %H:%M:%S"
FILE = paths.LOG


class Logger(object):

    def __init__(self):
        self._handler = None
        logging.basicConfig()

    def get_logger(self, name):
        if self._handler is None:
            handler = logging.FileHandler(FILE, mode='w')
            fmt = logging.Formatter(fmt=FORMAT, datefmt=FORMAT_TIME)
            handler.setFormatter(fmt)
            self._handler = handler
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._handler)
        return logger


def get_logger(name):
    return Logger().get_logger(name)