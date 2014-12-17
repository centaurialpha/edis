# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import time
import sys
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
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

# Módulos EDIS
#from edis import recursos
from src.helpers import (
    configuraciones,
    manejador_de_archivo
    )
from src.ui.contenedores.output import salida_compilador
from src.ui.dialogos.preferencias import preferencias_compilacion as pc

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
        self.connect(self.proceso_compilacion,
                    SIGNAL("error(QProcess::ProcessError)"),
                    self.ejecucion_error)

    def correr_compilacion(self, nombre_archivo=''):
        """ Se corre el comando gcc para la compilación """

        # Dirección del archivo a compilar
        self.nombre_archivo = nombre_archivo
        # Nombre del archivo sin extensión
        if not _TUX:
            self.ejecutable = (
                self.nombre_archivo.split('\\')[-1]).split('.')[0]
        else:
            self.ejecutable = (self.nombre_archivo.split('/')[-1]).split('.')[0]
        self.output.setCurrentCharFormat(self.output.formato_ok)
        # Para generar el ejecutable en la carpeta del fuente
        directorio_archivo = manejador_de_archivo.devolver_carpeta(
            self.nombre_archivo)
        self.proceso_compilacion.setWorkingDirectory(directorio_archivo)

        # Parámetros adicionales
        parametros_add = list(str(configuraciones.PARAMETROS).split())
        pref_compilador = pc.ECTab(self).configCompilacion
        checkEnsamblador = pref_compilador.checkEnsamblado

        # Ens = Verdadero si se activó la opción checkEnsamblador.
        ensamblador = {'Ens': True if checkEnsamblador.isChecked() else False}

        self.output.setPlainText(
            'Compilando archivo: %s\nDirectorio: %s ( %s )\n' %
            (self.nombre_archivo.split('/')[-1] if _TUX
            else self.nombre_archivo.split('\\')[-1], self.nombre_archivo,
                time.ctime()))
        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)

        # Comenzar proceso
        #FIXME: moverlo a un check temporal (?
        if not ensamblador['Ens']:
            parametros_gcc = ['-Wall', '-o']
            inicio = time.time()
            self.proceso_compilacion.start('gcc',
                                        parametros_gcc + [self.ejecutable] +
                                        parametros_add + [self.nombre_archivo])
            fin = time.time()
            #FIXME: test!
            self.tiempo = fin - inicio
        else:
            parametros_gcc = ['-Wall']
            self.proceso_compilacion.start('gcc', parametros_gcc +
                parametros_add + [self.nombre_archivo])
        #FIXME: revisar!
        self.compilado = True

    def ejecucion_terminada(self, codigoError, exitStatus):
        """ valores de codigoError
            0 = Cuando se compila bien, aún con advertencias
            1 = Error en la compilación
        """
        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setFontPointSize(11)
        formato_tiempo = QTextCharFormat()
        formato_tiempo.setForeground(QBrush(QColor("#007c00")))
        formato_tiempo.setFontPointSize(9)

        self.output.textCursor().insertText('\n\n')
        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(QBrush(QColor('#007c00')))
            self.output.textCursor().insertText(
                self.trUtf8("¡COMPILACIÓN EXITOSA! "), formato)
            self.output.textCursor().insertText(
                str(self.trUtf8("(tiempo total: %.4f segundos)")) %
                            self.tiempo, formato_tiempo)

        else:
            formato.setForeground(QBrush(QColor('red')))
            self.output.textCursor().insertText(
                self.trUtf8("¡LA COMPILACIÓN HA FALLADO!"), formato)
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_error(self, error):
        self.proceso_compilacion.kill()
        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setForeground(Qt.red)
        if error == 0:
            self.output.textCursor().insertText(
                self.trUtf8("Error: no se encuentra el compilador."), formato)
        else:
            self.output.textCursor().insertText(self.trUtf8(
                "Error proceso: %d" % error), formato)

    def correr_programa(self):
        """ Se encarga de correr el programa objeto generado """

        direc = manejador_de_archivo.devolver_carpeta(self.nombre_archivo)
        self.proceso_ejecucion.setWorkingDirectory(direc)

        if _TUX:
            terminal = configuraciones.TERMINAL
            bash = '%s -e "bash -c ./%s;read n"' % (terminal, self.ejecutable)
            # Run !
            self.proceso_ejecucion.start(bash)
        else:
            #FIXME: güindous!
            pass
            #self.pro = Popen(direc + '/' + self.ejecutable,
                #creationflags=CREATE_NEW_CONSOLE)

    def terminar_proceso(self):
        """ Termina el proceso """

        pass