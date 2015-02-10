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
    QColor,
    QMessageBox,
    QItemSelectionModel
    )

# Módulos QtCore
from PyQt4.QtCore import (
    QProcess,
    QDir,
    Qt,
    SIGNAL
    )

# Módulos EDIS
from src.helpers import configuracion
from src.ui.contenedores.output import salida
from src import paths

PATH_GCC = os.path.join(paths.PATH, "gcc", "bin", "gcc.exe")
GCC = 'gcc' if sys.platform.startswith('linux') else PATH_GCC


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

        self.output.clear()
        if codigo_error == 1:
            error1 = salida.Item(self.tr("El proceso ha sido frenado"))
            error1.setForeground(Qt.blue)
            self.output.addItem(error1)
        else:
            error = salida.Item(self.tr("Ha ocurrido un error en la ejecución. "
                                "Código de error: %s" % codigo_error))
            error.setForeground(Qt.red)
            self.output.addItem(error)

    def correr_compilacion(self, nombre_archivo=''):
        """ Se corre el comando gcc para la compilación """

        # Ejecutable
        directorio = QDir.fromNativeSeparators(nombre_archivo)
        self.ejecutable = directorio.split('/')[-1].split('.')[0]

        # Generar el ejecutable en el directorio del código fuente
        directorio_ejecutable = os.path.dirname(directorio)
        self.proceso_compilacion.setWorkingDirectory(directorio_ejecutable)

        self.output.clear()
        item = salida.Item(self.tr(
                           "Compilando archivo: %s ( %s )" %
                           (directorio.split('/')[-1], nombre_archivo)))
        self.output.addItem(item)

        gcc = GCC
        parametros_gcc = ['-Wall', '-o']
        self.proceso_compilacion.start(gcc, parametros_gcc +
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
            item_ok.setForeground(QColor("#0046cc"))
            self.output.addItem(item_ok)
        else:
            item_error = salida.Item(self.tr("¡LA COMPILACIÓN HA FALLADO!"))
            item_error.setForeground(Qt.red)
            self.output.addItem(item_error)
        count = self.output.count()
        self.output.setCurrentRow(count - 1, QItemSelectionModel.NoUpdate)

    def _error_compilacion(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        texto = salida.Item(self.tr("Ha ocurrido un error: quizás el compilador"
                            " no está instalado."))
        texto.setForeground(Qt.red)
        self.output.addItem(texto)

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