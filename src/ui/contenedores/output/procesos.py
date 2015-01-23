# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import time
import sys
import os
from subprocess import Popen
if sys.platform == 'win32':
    from subprocess import CREATE_NEW_CONSOLE

# Módulos QtGui
from PyQt4.QtGui import (
    QVBoxLayout,
    QWidget,
    QTextCharFormat,
    QTextCursor,
    QColor,
    QBrush,
    QMessageBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    QProcess,
    QDir
    )

# Módulos EDIS
from src import recursos
from src.helpers import configuracion
from src.ui.contenedores.output import salida_compilador


class EjecutarWidget(QWidget):

    _script = '%s -e "bash -c ./%s;echo;echo;echo;echo -n Presione \<Enter\> '\
    'para salir.;read I"'

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
        self.proceso_ejecucion.error[QProcess.ProcessError].connect(
            self._ejecucion_terminada)

    def _ejecucion_terminada(self, codigo_error):
        """ Éste método es ejecutado cuando la ejecución es frenada por el
        usuario o algún otro error. """

        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setFontPointSize(12)
        formato.setForeground(QColor(recursos.TEMA['error']))
        #formato.setBackground(QColor('red'))
        self.output.setCurrentCharFormat(formato)
        if codigo_error == 1:
            self.output.setPlainText(self.tr("El proceso ha sido frenado."))
        else:
            self.output.setPlainText(self.tr(
                                    "Ha ocurrido un error en la ejecución. "
                                    "Código de error: %s" % codigo_error))

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
        self.proceso_compilacion.waitForFinished()

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
        self.output.textCursor().insertText('\n')

        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(QBrush(QColor('#0197fd')))
            self.output.textCursor().insertText(
                self.trUtf8("¡COMPILACIÓN EXITOSA! "), formato)
        else:
            formato.setForeground(QBrush(QColor('red')))
            self.output.textCursor().insertText(
                self.tr("¡LA COMPILACIÓN HA FALLADO!"), formato)

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
        """ Ejecuta el binario generado por el compilador """

        direc = os.path.dirname(archivo)
        self.proceso_ejecucion.setWorkingDirectory(direc)

        if configuracion.LINUX:
            terminal = configuracion.ESettings.get('terminal')
            if not terminal:
                QMessageBox.warning(self, self.tr("Advertencia"),
                                    self.tr("No se ha configurado una terminal"
                                    " para ejecutar el binario."))
                return
            proceso = 'xterm -T "%s" -e /usr/bin/cb_console_runner "%s"' \
                    % (self.ejecutable, os.path.join(direc, self.ejecutable))
            # Run !
            self.proceso_ejecucion.start(proceso)
        else:
            #FIXME: Usar QProcess
            Popen([os.path.join(direc, self.ejecutable)],
                    creationflags=CREATE_NEW_CONSOLE)

    def compilar_ejecutar(self, archivo):
        self.correr_compilacion(archivo)
        self.correr_programa(archivo)

    def limpiar(self, archivo):
        """ Elimina el binario generado por la compilación """

        if archivo is None:
            return
        binario = archivo.split('.')[0]
        if configuracion.WINDOWS:
            binario = binario + '.exe'
        os.remove(binario)

    def terminar_proceso(self):
        """ Termina el proceso """

        self.proceso_ejecucion.kill()