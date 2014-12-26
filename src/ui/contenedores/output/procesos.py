# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import time
import sys
import os
from subprocess import Popen
from subprocess import PIPE
if sys.platform == 'win32':
    from subprocess import CREATE_NEW_CONSOLE

# Módulos QtGui
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush
#from PyQt4.QtGui import QFont

# Módulos QtCore
from PyQt4.QtCore import (
    QProcess,
    SIGNAL,
    Qt,
    QDir
    )

# Módulos EDIS
#from edis import recursos
from src.helpers import (
    configuraciones,
    manejador_de_archivo
    )
from src.ui.contenedores.output import salida_compilador

_TUX = configuraciones.LINUX


class EjecutarWidget(QWidget):

    def __init__(self):
        super(EjecutarWidget, self).__init__()
        self.compilado = False
        self.tiempo = 0.0
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        self.output = salida_compilador.SalidaWidget(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Procesos
        self.proceso_compilacion = QProcess(self)
        self.proceso_ejecucion = QProcess(self)

        # Conexión
        self.proceso_compilacion.readyReadStandardError.connect(
            self.output.parser_salida_stderr)
        self.proceso_compilacion.finished[int, QProcess.ExitStatus].connect(
            self.ejecucion_terminada)
        self.proceso_compilacion.error[QProcess.ProcessError].connect(
            self._error_compilacion)

    def correr_compilacion(self, nombre_archivo=''):
        """ Se corre el comando gcc para la compilación """

        # Ejecutable
        self.output.setCurrentCharFormat(self.output.formato_ok)
        directorio = QDir.fromNativeSeparators(nombre_archivo)
        self.ejecutable = directorio.split('/')[-1].split('.')[0]

        # Generar el ejecutable en el directorio del código fuente
        directorio_ejecutable = os.path.dirname(directorio)
        self.proceso_compilacion.setWorkingDirectory(directorio_ejecutable)

        self.output.setPlainText(
            "Compilando archivo: %s\nDirectorio: %s ( %s )\n" %
            (directorio.split('/')[-1], nombre_archivo, time.ctime()))

        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)

        parametros_gcc = ['-Wall', '-o']
        self.proceso_compilacion.start('gcc', parametros_gcc +
                                        [self.ejecutable] + [nombre_archivo])

    def ejecucion_terminada(self, codigoError, exitStatus):
        """
        Cuando la compilación termina @codigoError toma dos valores:
            0 = La compilación ha terminado de forma correcta
            1 = La compilación ha fallado

        """

        # Formato para el texto
        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setFontPointSize(11)
        formato_tiempo = QTextCharFormat()
        formato_tiempo.setForeground(QBrush(QColor("#007c00")))
        formato_tiempo.setFontPointSize(9)
        self.output.textCursor().insertText('\n')

        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(QBrush(QColor('#007c00')))
            self.output.textCursor().insertText(
                self.trUtf8("¡COMPILACIÓN EXITOSA! "), formato)
            self.output.textCursor().insertText(
                self.tr("(tiempo total: %.4f segundos)") %
                            self.tiempo, formato_tiempo)

        else:
            formato.setForeground(QBrush(QColor('red')))
            self.output.textCursor().insertText(
                self.tr("¡LA COMPILACIÓN HA FALLADO!"), formato)
        self.output.moveCursor(QTextCursor.Down)

    def _error_compilacion(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setForeground(QBrush(QColor('red')))
        self.output.textCursor().insertText(
            self.tr("Ha ocurrido un error: Quizás el compilador "
                    "no está presente"), formato)

    def correr_programa(self, archivo):
        """ Se encarga de correr el programa objeto generado """

        direc = os.path.dirname(archivo)
        self.proceso_ejecucion.setWorkingDirectory(direc)

        if _TUX:
            #FIXME: Terminal
            terminal = configuraciones.TERMINAL
            bash = '%s -e "bash -c ./%s;read n"' % (terminal, self.ejecutable)
            # Run !
            self.proceso_ejecucion.start(bash)
        else:
            #FIXME: Usar QProcess
            Popen([os.path.join(direc, self.ejecutable)],
                    creationflags=CREATE_NEW_CONSOLE)

    def terminar_proceso(self):
        """ Termina el proceso """

        self.proceso_ejecucion.kill()