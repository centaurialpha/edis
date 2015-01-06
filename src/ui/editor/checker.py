# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Checker usa la herramienta 'cppcheck' (http://cppcheck.sourceforge.net/)


from subprocess import Popen, PIPE

from PyQt4.QtCore import (
    QThread,
    pyqtSignal
    )

from src.helpers import logger

log = logger.edisLogger('checker')

#TODO: Cambiar mensajes a español


class Checker(QThread):

    # Señales
    errores = pyqtSignal(dict)

    def __init__(self, editor):
        super(Checker, self).__init__()
        self._editor = editor
        self._errores = {}

    def run(self):
        try:
            proceso = Popen(self._cppcheck + self._parametros + [self._archivo],
                            stdout=PIPE, stderr=PIPE, shell=False)
            salida = proceso.communicate()[1]
            self._parsear(salida)
        except Exception as error:
            log.error("Ha ocurrido un error: %s" % error)

    def _parsear(self, salida):
        for l in salida.splitlines():
            l = str(l).split(';')
            linea = int(l[0].split('"')[-1]) - 1
            tipo = l[1]
            mensaje = l[2].replace('\\', '').split('.')[0]
            if not linea in self._errores:
                self._errores[linea] = (tipo, mensaje)
        self.errores.emit(self._errores)

    def _restart(self):
        self._errores.clear()

    def tooltip(self, linea):
        tool = self._errores.get(linea, None)
        if tool is not None:
            return self._errores.get(linea)[-1]

    def tipo(self, linea):
        return self._errores.get(linea)[0]

    def run_cppcheck(self, archivo):
        self._archivo = archivo
        self._cppcheck = ['cppcheck']
        self._parametros = ['--enable=warning,unusedFunction,style,portability,'
                            'performance', '--template="{line};{severity};'
                            '{message}"', '--language=c']
        self._restart()
        self.start()