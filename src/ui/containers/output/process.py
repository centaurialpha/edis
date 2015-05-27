# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
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
    Qt,
    SIGNAL
    )

# Módulos EDIS
from src.core import (
    paths,
    settings,
    logger
    )
from src.ui.containers.output import output_compiler

log = logger.get_logger(__name__)
ERROR = log.error

ENV_GCC = os.path.join(paths.PATH, "gcc", "bin")


class EjecutarWidget(QWidget):

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

        # Conexiones
        self.build_process.readyReadStandardError.connect(
            self.output.stderr_output)
        self.build_process.finished[int, QProcess.ExitStatus].connect(
            self._compilation_finished)
        self.build_process.error[QProcess.ProcessError].connect(
            self._compilation_error)
        self.execution_process.finished[int, QProcess.ExitStatus].connect(
            self._execution_finished)

    def _execution_finished(self, code, status):
        if status == QProcess.CrashExit:
            text = output_compiler.Item(
                self.tr("La ejecución se ha interrumpido"))
            text.setForeground(Qt.red)
            self.output.addItem(text)
        else:
            text = output_compiler.Item(
                self.tr("Ejecución Exitosa!"))
            text.setForeground(QColor("#7FE22A"))
            self.output.addItem(text)

    def run_compilation(self, sources):
        """ Se corre el comando gcc para la compilación """

        # Ejecutable
        filename, files = sources
        if not files:
            # No es un proyecto
            files = [filename]
        path = QDir.fromNativeSeparators(filename)
        self.exe = os.path.splitext(os.path.basename(path))[0]

        # Generar el ejecutable en el directorio del código fuente
        exe_path = os.path.dirname(path)
        self.build_process.setWorkingDirectory(exe_path)

        # Se limpia el QListWidget
        self.output.clear()

        flags = settings.COMPILER_FLAGS.split()
        params = ['-o', self.exe] + flags
        gcc = 'gcc'
        if not sys.platform.startswith("linux"):
            gcc = os.path.join(self._environment, 'gcc')

        item = output_compiler.Item(
            self.tr(">>> Compilando: {0} ( en directorio {1} )").format(
                    path.split('/')[-1], exe_path))
        self.output.addItem(item)
        self.output.addItem(output_compiler.Item(
            self.tr(">>> Comando: {0}").format(
                gcc + ' ' + ' '.join(params) + ' ' + ' '.join(files))))

        # Se inicia el proceso
        self.build_process.start(gcc, params + files)
        self.build_process.waitForFinished()

    def _compilation_finished(self, code, status):
        """
        Cuando la compilación termina @codigoError toma dos valores:
            0 = La compilación ha terminado de forma correcta
            1 = La compilación ha fallado

        """

        if status == QProcess.NormalExit and code == 0:
            self._compilation_failed = False
            item_ok = output_compiler.Item(
                self.tr("¡LA COMPILACIÓN HA SIDO EXITOSA!"))
            self.output.addItem(item_ok)
            item_ok.setForeground(QColor("#7FE22A"))
        else:
            self._compilation_failed = True
            item_error = output_compiler.Item(
                self.tr("¡LA COMPILACIÓN HA FALLADO!"))
            item_error.setForeground(QColor("#E20000"))
            self.output.addItem(item_error)
        syntax_ok = True if code == 0 else False
        self.emit(SIGNAL("updateSyntaxCheck(bool)"), syntax_ok)
        code_status = output_compiler.Item(
                self.tr("Proceso terminado con código: {0}").format(code),
                italic=True)
        self.output.addItem(code_status)
        count = self.output.count()
        self.output.setCurrentRow(count - 1, QItemSelectionModel.NoUpdate)

    def _compilation_error(self, error):
        """
        Éste método se ejecuta cuando el inicio del proceso de compilación
        falla. Una de las causas puede ser la ausencia del compilador.

        """

        text = output_compiler.Item(
            self.tr("Se ha producido un error. Compilador no encontrado."))
        text.setForeground(Qt.red)
        self.output.addItem(text)

    def run_program(self, sources):
        """ Ejecuta el binario generado por el compilador """

        path = os.path.dirname(sources[0])
        self.execution_process.setWorkingDirectory(path)
        # Path ejecutable
        path_exe = os.path.join(path, self.exe)
        if not settings.IS_LINUX:
            path_exe += '.exe'
        # Si no existe se termina el proceso
        if not self._check_file_exists(path_exe):
            text = output_compiler.Item(
                self.tr("El archivo no existe: {0}").format(path_exe))
            text.setForeground(Qt.red)
            self.output.addItem(text)
            return
        # Texto en la salida
        text = output_compiler.Item(
            self.tr("Ejecutando... {0}").format(path_exe))
        self.output.addItem(text)

        if settings.IS_LINUX:
            # Run !
            terminal = settings.get_setting('terminal')
            arguments = [os.path.join(paths.PATH, "tools",
                         "run_script.sh %s" % path_exe)]
            self.execution_process.start(terminal, ['-e'] + arguments)
        else:
            pauser = os.path.join(paths.PATH, "tools", "pauser",
                                  "system_pause.exe")
            process = [pauser] + ["\"%s\"" % path_exe]
            Popen(process, creationflags=CREATE_NEW_CONSOLE)

    def _check_file_exists(self, exe):
        """ Comprueba si el ejecutable existe """

        exists = True
        if not os.path.exists(exe):
            exists = False
        return exists

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
        if not settings.IS_LINUX:
            binary += '.exe'
        os.remove(binary)

    def kill_process(self):
        """ Termina el proceso """

        self.execution_process.kill()
