# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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
    #QMessageBox,
    QItemSelectionModel
    )

# Módulos QtCore
from PyQt4.QtCore import (
    QProcess,
    QProcessEnvironment,
    QDir,
    Qt
    )

# Módulos EDIS
from src.helpers import configurations
from src.ui.containers.output import output_compiler
from src import paths
from src.helpers import logger

log = logger.edis_logger.get_logger(__name__)
ERROR = log.error

ENV_GCC = os.path.join(paths.PATH, "gcc", "bin")


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
        self.output = output_compiler.SalidaCompilador(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Procesos
        self.proceso_compilacion = QProcess(self)
        if not sys.platform.startswith('linux'):
            self._envgcc = QProcessEnvironment.systemEnvironment()
            self._envgcc.insert("PATH", ENV_GCC)
            self.proceso_compilacion.setProcessEnvironment(self._envgcc)
        self.proceso_ejecucion = QProcess(self)

        # Conexión
        self.proceso_compilacion.readyReadStandardError.connect(
            self.output.parsear_salida_stderr)
        self.proceso_compilacion.finished[int, QProcess.ExitStatus].connect(
            self.ejecucion_terminada)
        self.proceso_compilacion.error[QProcess.ProcessError].connect(
            self._error_compilacion)
        self.proceso_ejecucion.error[QProcess.ProcessError].connect(
            self._ejecucion_terminada)

    def _ejecucion_terminada(self, codigo_error):
        """ Éste método es ejecutado cuando la ejecución es frenada por el
        usuario o algún otro error. """

        self.output.clear()
        if codigo_error == 1:
            error1 = output_compiler.Item(self.tr("The process terminated"))
            error1.setForeground(Qt.red)
            self.output.addItem(error1)
        else:
            error = output_compiler.Item(self.tr("An error has occurred. "
                                         "Error code: {0}").format(
                                         codigo_error))
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
        item = output_compiler.Item(self.tr(
                                    "Building file: {0} ( {1} )".format(
                                    directorio.split('/')[-1], nombre_archivo)))
        self.output.addItem(item)

        parametros_gcc = ['-Wall', '-o']
        gcc = 'gcc'
        if not sys.platform.startswith("linux"):
            gcc = os.path.join(self._environment, 'gcc')
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
            item_ok = output_compiler.Item(
                self.tr("¡COMPILATION FINISHED SUCCESSFULLY!"))
            item_ok.setForeground(QColor("#a6e22e"))
            self.output.addItem(item_ok)
        else:
            item_error = output_compiler.Item(self.tr("¡COMPILATION FAILED!"))
            item_error.setForeground(QColor("#e73e3e"))
            self.output.addItem(item_error)
        count = self.output.count()
        self.output.setCurrentRow(count - 1, QItemSelectionModel.NoUpdate)

    def _error_compilacion(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        texto = output_compiler.Item(
            self.tr("An error has occurred: Compiler not found."))
        texto.setForeground(Qt.red)
        self.output.addItem(texto)

    def correr_programa(self, archivo):
        """ Ejecuta el binario generado por el compilador """

        #FIXME: Agregar terminal por defecto
        direc = os.path.dirname(archivo)
        self.proceso_ejecucion.setWorkingDirectory(direc)

        if configurations.LINUX:
            proceso = 'xterm -T "%s" -e /usr/bin/cb_console_runner "%s"' \
                      % (self.ejecutable, os.path.join(direc, self.ejecutable))
            # Run !
            self.proceso_ejecucion.start(proceso)
        else:
            pauser = os.path.join(paths.PATH, "tools", "pauser",
                                  "system_pause.exe")
            process = pauser + ' ' + os.path.join(direc, self.ejecutable)
            Popen(process, creationflags=CREATE_NEW_CONSOLE)

    @property
    def _environment(self):
        """ Devuelve la variable de entorno gcc """

        return self._envgcc.value("PATH", "")

    def compilar_ejecutar(self, archivo):
        self.correr_compilacion(archivo)
        self.correr_programa(archivo)

    def limpiar(self, archivo):
        """ Elimina el binario generado por la compilación """

        if archivo is None:
            return
        binario = archivo.split('.')[0]
        if configurations.WINDOWS:
            binario = binario + '.exe'
        os.remove(binario)

    def terminar_proceso(self):
        """ Termina el proceso """

        self.proceso_ejecucion.kill()