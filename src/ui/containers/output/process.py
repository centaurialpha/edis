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
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        self.output = output_compiler.SalidaCompilador(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Procesos
        self.process = QProcess(self)
        if not sys.platform.startswith('linux'):
            self._envgcc = QProcessEnvironment.systemEnvironment()
            self._envgcc.insert("PATH", ENV_GCC)
            self.process.setProcessEnvironment(self._envgcc)
        self.proceso_ejecucion = QProcess(self)

        # Conexión
        self.process.readyReadStandardError.connect(
            self.output.parsear_salida_stderr)
        self.process.finished[int, QProcess.ExitStatus].connect(
            self.ejecucion_terminada)
        self.process.error[QProcess.ProcessError].connect(
            self._error_compilacion)
        self.proceso_ejecucion.error[QProcess.ProcessError].connect(
            self._ejecucion_terminada)

    def _ejecucion_terminada(self, error_code):
        """ Éste método es ejecutado cuando la ejecución es frenada por el
        usuario o algún otro error. """

        self.output.clear()
        if error_code == 1:
            error1 = output_compiler.Item(self.tr("The process terminated"))
            error1.setForeground(Qt.red)
            self.output.addItem(error1)
        else:
            error = output_compiler.Item(self.tr("An error has occurred. "
                                         "Error code: {0}").format(
                                         error_code))
            error.setForeground(Qt.red)
            self.output.addItem(error)

    def run_compilation(self, filename=''):
        """ Se corre el comando gcc para la compilación """

        # Ejecutable
        path = QDir.fromNativeSeparators(filename)
        self.exe = os.path.splitext(os.path.basename(path))[0]

        # Generar el ejecutable en el directorio del código fuente
        exe_path = os.path.dirname(path)
        self.process.setWorkingDirectory(exe_path)

        self.output.clear()
        item = output_compiler.Item(self.tr(
                                    "Building file: {0} ( {1} )".format(
                                    path.split('/')[-1], filename)))
        self.output.addItem(item)

        params = ['-Wall', '-o']
        gcc = 'gcc'
        if not sys.platform.startswith("linux"):
            gcc = os.path.join(self._environment, 'gcc')
        self.process.start(gcc, params + [self.exe] + [filename])
        self.process.waitForFinished()

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

    def run_program(self, archivo):
        """ Ejecuta el binario generado por el compilador """

        #FIXME: Agregar terminal por defecto
        direc = os.path.dirname(archivo)
        self.proceso_ejecucion.setWorkingDirectory(direc)

        if configurations.LINUX:
            proceso = 'xterm -T "%s" -e /usr/bin/cb_console_runner "%s"' \
                      % (self.exe, os.path.join(direc, self.exe))
            # Run !
            self.proceso_ejecucion.start(proceso)
        else:
            try:
                pauser = os.path.join(paths.PATH, "tools", "pauser",
                                      "system_pause.exe")
                path_exe = os.path.join(direc, self.exe)
                process = [pauser] + ["\"%s\"" % path_exe]
                Popen(process, creationflags=CREATE_NEW_CONSOLE)
            except Exception as reason:
                print(reason)
                ERROR('Error: %s', reason)

    @property
    def _environment(self):
        """ Devuelve la variable de entorno gcc """

        return self._envgcc.value("PATH", "")

    def build_and_run(self, archivo):
        self.run_compilation(archivo)
        self.run_program(archivo)

    def clean(self, archivo):
        """ Elimina el binario generado por la compilación """

        if archivo is None:
            return
        binario = archivo.split('.')[0]
        if configurations.WINDOWS:
            binario = binario + '.exe'
        os.remove(binario)

    def kill_process(self):
        """ Termina el proceso """

        self.proceso_ejecucion.kill()