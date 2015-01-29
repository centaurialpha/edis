# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
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
    QColor,
    QBrush,
    QMessageBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    QProcess,
    QDir,
    Qt,
    SIGNAL
    )

# Módulos EDIS
from src import paths
from src.helpers import configuracion
from src.ui.contenedores.output import salida


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
        self.output = salida.SalidaCompilador(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Procesos
        self.proceso_compilacion = QProcess(self)
        self.proceso_ejecucion = QProcess(self)

        # Conexión
        self.output.ir_a_linea.connect(self._emitir_ir_a_linea)
        self.proceso_compilacion.readyReadStandardError.connect(
            self.output.parsear_salida_stderr)
        self.proceso_compilacion.finished[int, QProcess.ExitStatus].connect(
            self.ejecucion_terminada)
        self.proceso_compilacion.error[QProcess.ProcessError].connect(
            self._error_compilacion)
        self.proceso_ejecucion.error[QProcess.ProcessError].connect(
            self._ejecucion_terminada)

    def _emitir_ir_a_linea(self, linea):
        self.emit(SIGNAL("ir_a_linea(int)"), linea)

    def _ejecucion_terminada(self, codigo_error):
        """ Éste método es ejecutado cuando la ejecución es frenada por el
        usuario o algún otro error. """

        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setFontPointSize(12)
        formato.setForeground(QColor(paths.TEMA['error']))
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
        directorio = QDir.fromNativeSeparators(nombre_archivo)
        self.ejecutable = directorio.split('/')[-1].split('.')[0]

        # Generar el ejecutable en el directorio del código fuente
        directorio_ejecutable = os.path.dirname(directorio)
        self.proceso_compilacion.setWorkingDirectory(directorio_ejecutable)

        self.output.clear()
        self.output.addItem(self.tr(
                            "Compilando archivo: %s ( %s )" %
                            (directorio.split('/')[-1], nombre_archivo)))

        clang = 'clang'
        parametros_clang = ['-Wall', '-o']
        self.proceso_compilacion.start(clang, parametros_clang +
                                        [self.ejecutable] + [nombre_archivo])
        self.proceso_compilacion.waitForFinished()

    def ejecucion_terminada(self, codigoError, exitStatus):
        """
        Cuando la compilación termina @codigoError toma dos valores:
            0 = La compilación ha terminado de forma correcta
            1 = La compilación ha fallado

        """

        if exitStatus == QProcess.NormalExit and codigoError == 0:
            item_ok = salida.Item(self.tr("¡COMPILACIÓN EXITOSA!"))
            item_ok.clickeable = False
            item_ok.setForeground(QColor("#0046cc"))
            self.output.addItem(item_ok)
        else:
            item_error = salida.Item(self.tr("¡LA COMPILACIÓN HA FALLADO!"))
            item_error.clickeable = False
            item_error.setForeground(Qt.red)
            self.output.addItem(item_error)

    def _error_compilacion(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        #FIXME
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