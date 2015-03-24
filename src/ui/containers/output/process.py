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
from src.helpers import settings
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

        # Flag
        self._compilation_failed = False

        # Procesos
        self.build_process = QProcess(self)
        if not sys.platform.startswith('linux'):
            self._envgcc = QProcessEnvironment.systemEnvironment()
            self._envgcc.insert("PATH", ENV_GCC)
            self.build_process.setProcessEnvironment(self._envgcc)
        self.execution_process = QProcess(self)

        # Conexión
        self.build_process.readyReadStandardError.connect(
            self.output.stderr_output)
        self.build_process.finished[int, QProcess.ExitStatus].connect(
            self._compilation_finished)
        self.build_process.error[QProcess.ProcessError].connect(
            self._compilation_error)
        self.execution_process.error[QProcess.ProcessError].connect(
            self._terminate_execution)

    def _terminate_execution(self, error_code):
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
        self.build_process.setWorkingDirectory(exe_path)

        self.output.clear()
        item = output_compiler.Item(self.tr(
            ">>> Building file: {0} ( {1} )".format(
                path.split('/')[-1], filename)))

        self.output.addItem(item)

        params = ['-Wall', '-o']
        gcc = 'gcc'
        if not sys.platform.startswith("linux"):
            gcc = os.path.join(self._environment, 'gcc')
        self.build_process.start(gcc, params + [self.exe] + [filename])
        self.build_process.waitForFinished()

    def _compilation_finished(self, codigoError, exitStatus):
        """
        Cuando la compilación termina @codigoError toma dos valores:
            0 = La compilación ha terminado de forma correcta
            1 = La compilación ha fallado

        """

        if exitStatus == QProcess.NormalExit and codigoError == 0:
            self._compilation_failed = False
            item_ok = output_compiler.Item(
                self.tr("¡COMPILATION FINISHED SUCCESSFULLY!"))
            item_ok.setForeground(QColor("#7FE22A"))
            self.output.addItem(item_ok)
        else:
            self._compilation_failed = True
            item_error = output_compiler.Item(self.tr("¡COMPILATION FAILED!"))
            item_error.setForeground(QColor("#E20000"))
            self.output.addItem(item_error)
        count = self.output.count()
        self.output.setCurrentRow(count - 1, QItemSelectionModel.NoUpdate)

    def _compilation_error(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        text = output_compiler.Item(
            self.tr("An error has occurred: Compiler not found."))
        text.setForeground(Qt.red)
        self.output.addItem(text)

    def run_program(self, archivo):
        """ Ejecuta el binario generado por el compilador """

        # FIXME: Agregar terminal por defecto
        path = os.path.dirname(archivo)
        self.execution_process.setWorkingDirectory(path)

        if settings.IS_LINUX:
            # Run !
            terminal = settings.get_setting('terminal')
            arguments = [os.path.join(os.path.dirname(__file__),
                         "run_script.sh %s" % os.path.join(path, self.exe))]
            self.execution_process.start(terminal, ['-e'] + arguments)
        else:
            pauser = os.path.join(paths.PATH, "tools", "pauser",
                                  "system_pause.exe")
            path_exe = os.path.join(path, self.exe)
            process = [pauser] + ["\"%s\"" % path_exe]
            Popen(process, creationflags=CREATE_NEW_CONSOLE)

    @property
    def _environment(self):
        """ Devuelve la variable de entorno gcc """

        return self._envgcc.value("PATH", "")

    def build_and_run(self, archivo):
        self.run_compilation(archivo)
        if not self._compilation_failed:
            self.run_program(archivo)

    def clean(self, exe):
        """ Elimina el binario generado por la compilación """

        if exe is None:
            return
        binary = exe.split('.')[0]
        if settings.IS_WINDOWS:
            binary += '.exe'
        os.remove(binary)

    def kill_process(self):
        """ Termina el proceso """

        self.execution_process.kill()
