# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
import os
from subprocess import Popen, PIPE
if sys.platform == 'win32':
    from subprocess import (
        STARTUPINFO,
        SW_HIDE,
        STARTF_USESHOWWINDOW
        )
from src import paths
from src.helpers import (
    logger,
    configuracion
    )

log = logger.edis_logger.get_logger(__name__)
WARNING = log.warning


class Ctags(object):

    def __init__(self):
        pass

    def run_ctags(self, archivo):
        info_ctags = list()

        comando = self.path_ejecutable()
        parametros = ['--excmd=number', '-f -', '--fields=fimKsSzt', archivo]

        if configuracion.WINDOWS:
            # Flags para ocultar cmd
            si = STARTUPINFO()
            si.dwFlags |= STARTF_USESHOWWINDOW
            si.wShowWindow = SW_HIDE
            proceso = Popen(comando + parametros, stdout=PIPE,
                            startupinfo=si)
        else:
            try:
                proceso = Popen(comando + parametros, stdout=PIPE)
            except Exception:
                WARNING('Ctags no está instalado!')
                proceso = None
        if proceso is not None:
            salida = proceso.communicate()[0]
            for linea in salida.splitlines():
                info = linea.decode('utf-8').split('\t')
                info[2] = info[2].replace(';"', '')
                info[3] = info[3].replace('kind:', '')
                info_ctags.append(info)
            return info_ctags

    def parser(self, salida):
        if salida is None:
            return
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
        exe = ''
        if sys.platform == 'linux':
            exe = 'ctags'
        else:
            exe = os.path.join(paths.PATH, "ectags", "ctags.exe")
        return [exe]