# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Checker usa la herramienta 'cppcheck' (http://cppcheck.sourceforge.net/)

import sys
if sys.platform == 'win32':
    from subprocess import (
        STARTUPINFO,
        SW_HIDE,
        STARTF_USESHOWWINDOW
        )
from subprocess import Popen, PIPE

from PyQt4.QtCore import (
    QThread,
    pyqtSignal
    )

from src.helpers import (
    logger,
    configuracion
    )

log = logger.edisLogger('checker')

#TODO: Cambiar mensajes a español

# ID
UV = "unusedVariable"
URV = "unreadVariable"
UF = "unusedFunction"
AIOOB = "arrayIndexOutOfBounds"


class Checker(QThread):

    # Señales
    errores = pyqtSignal(dict)

    def __init__(self, editor):
        super(Checker, self).__init__()
        self._editor = editor
        self._errores = {}

    def run(self):
        try:
            #FIXME:
            if configuracion.WINDOWS:
                # Flags para ocultar cmd
                si = STARTUPINFO()
                si.dwFlags |= STARTF_USESHOWWINDOW
                si.wShowWindow = SW_HIDE
                proceso = Popen(self._cppcheck + self._parametros +
                                [self._archivo], stdout=PIPE, stderr=PIPE,
                                shell=False)
            else:
                proceso = Popen(self._cppcheck + self._parametros +
                                [self._archivo], stdout=PIPE, stderr=PIPE,
                                shell=False)

            salida = proceso.communicate()[1]
            self._parsear(salida)
        except Exception as error:
            log.error("Ha ocurrido un error: %s" % error)

    def _parsear(self, salida):
        for l in salida.splitlines():
            l = str(l).split(';')
            linea = int(l[0].split('"')[-1]) - 1
            tipo = l[1]
            mensaje = l[2]
            _id = l[-1].split('\"')[0]
            if _id == UV:
                variable = mensaje.split(':')[-1].strip()
                mensaje = Checker.variable_sin_usar(variable)
            if _id == UF:
                funcion = mensaje.split('\\\'')[1]
                mensaje = Checker.funcion_sin_usar(funcion)
            if _id == URV:
                variable = mensaje.split('\\\'')[1]
                mensaje = Checker.variable_asignada_sin_usar(variable)
            if _id == AIOOB:
                array = mensaje.split('\\\'')[1]
                indice = mensaje.split()[5]
                mensaje = Checker.indice_fuera_de_rango(array, indice)
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
                            '{message};{id}"', '--language=c']
        self._restart()
        self.start()

    @staticmethod
    def variable_sin_usar(variable):
        return "Variable sin usar: %s" % variable

    @staticmethod
    def variable_asignada_sin_usar(variable):
        mensaje = "Variable '%s', se le asigna un valor que nunca se utiliza."
        return mensaje % variable

    @staticmethod
    def funcion_sin_usar(funcion):
        return "La función '%s' no se utiliza nunca." % funcion

    @staticmethod
    def indice_fuera_de_rango(array, indice):
        mensaje = "Array: '%s'. indice %s fuera de rango."
        return mensaje % (array, indice)