# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
from subprocess import Popen, PIPE

from src import recursos
from src.helpers import logger

log = logger.edisLogger('ctags')


class Ctags(object):

    def __init__(self):
        pass

    def run_ctags(self, archivo):
        info_ctags = list()

        comando = self.path_ejecutable()
        parametros = ['--excmd=number', '-f -', '--fields=fimKsSzt', archivo]

        try:
            proceso = Popen(comando + parametros, stdout=PIPE)
            salida = proceso.communicate()[0]
            for linea in salida.splitlines():
                info = linea.decode('utf-8').split('\t')
                info[2] = info[2].replace(';"', '')
                info[3] = info[3].replace('kind:', '')
                info_ctags.append(info)
        except Exception as error:
            log.error("Error al ejecutar ctags.", error.args)
        return info_ctags

    def parser(self, salida):
        simbolos = {}

        for item in salida:
            nombre = item[0]
            linea = item[2]
            tipo = item[3]
            padre = ''
            if tipo == 'member':
                padre = item[4].split(':')[-1]
            if not tipo in simbolos:
                simbolos[tipo] = []
            simbolos[tipo].append(
                {'nombre': nombre, 'linea': linea, 'padre': padre})
        return simbolos

    def path_ejecutable(self):
        exe = 'ctags' if sys.platform == 'linux' else recursos.CTAGS
        if exe is None:
            #FIXME: think this!
            pass
        return [exe]