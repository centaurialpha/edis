# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import logging
from src import paths

FORMATO_LOG = "%(asctime)s %(name)10s %(levelname)10s %(message)10s"
FORMATO_TIEMPO = "%y-%m-%d %H:%M:%S"
ARCHIVO_LOG = paths.LOG


class Logger(object):

    def __init__(self):
        self.handler = None
        logging.basicConfig()

    def get_logger(self, nombre):
        if self.handler is None:
            handler = logging.FileHandler(ARCHIVO_LOG, mode='w')
            formato = logging.Formatter(fmt=FORMATO_LOG, datefmt=FORMATO_TIEMPO)
            handler.setFormatter(formato)
            self.handler = handler
        logger = logging.getLogger(nombre)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)
        return logger


edis_logger = Logger()