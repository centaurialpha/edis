#-*- coding: utf-8 -*-

# <Encargado de correr comandos de compilación, ejecución.>
# This file is part of EDIS-C.

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

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
from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.nucleo import manejador_de_archivo
from edis_c.interfaz.contenedor_secundario import salida_compilador
from edis_c.interfaz.dialogos.preferencias import preferencias_compilacion as pc

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

        # Proceso
        self.proceso = QProcess(self)
        self.pro = None

        # Conexión
        self.proceso.readyReadStandardOutput.connect(
            self.output.salida_estandar)
        self.proceso.readyReadStandardError.connect(
            self.output.parser_salida_stderr)
        self.proceso.readyReadStandardError.connect(
            self.output.datos_tabla)
        self.proceso.finished[int, QProcess.ExitStatus].connect(
            self.ejecucion_terminada)
        self.connect(self.proceso, SIGNAL("error(QProcess::ProcessError)"),
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
        self.proceso.setWorkingDirectory(directorio_archivo)

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
        self.output.moveCursor(QTextCursor.Down)
        self.output.textCursor().insertBlock()

        # Comenzar proceso
        #FIXME: moverlo a un check temporal (?
        if not ensamblador['Ens']:
            parametros_gcc = ['-Wall', '-o']
            inicio = time.time()
            self.proceso.start('gcc', parametros_gcc + [self.ejecutable] +
                parametros_add + [self.nombre_archivo])
            fin = time.time()
            #FIXME: test!
            self.tiempo = fin - inicio
        else:
            parametros_gcc = ['-Wall']
            self.proceso.start('gcc', parametros_gcc +
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
        #formato.setFontWeight(QFont.Bold)
        formato.setFontPointSize(11)
        formato_tiempo = QTextCharFormat()
        formato_tiempo.setForeground(QBrush(
            QColor(recursos.TEMA_EDITOR['salida-exitosa'])))
        formato_tiempo.setFontPointSize(9)

        self.output.textCursor().insertText('\n\n')
        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(
                QBrush(QColor(recursos.TEMA_EDITOR['salida-exitosa'])))
            self.output.textCursor().insertText(
                self.trUtf8("¡Compilación exitosa! "), formato)
            self.output.textCursor().insertText(
                str(self.trUtf8("(tiempo total: %.4f segundos)")) %
                            self.tiempo, formato_tiempo)

        else:
            formato.setForeground(
                QBrush(QColor(recursos.TEMA_EDITOR['salida-error'])))
            self.output.textCursor().insertText(
                self.trUtf8("No hubo compilación!"), formato)
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_error(self, error):
        self.proceso.kill()
        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setForeground(Qt.red)
        if error == 0:
            self.output.textCursor().insertText(self.trUtf8("Error!"), formato)
        else:
            self.output.textCursor().insertText(self.trUtf8(
                "Error proceso: %d" % error), formato)

    def correr_programa(self):
        """ Se encarga de correr el programa objeto generado """

        direc = manejador_de_archivo.devolver_carpeta(self.nombre_archivo)
        if _TUX:
            # Para nombres de carpeta con espacios (Linux)
            direc = direc.replace(' ', '\\ ')
        # Scripts en BASH para impedir que la terminal se cierre al ejecutar
        # el archivo objeto
        DASH = [
            '#!/bin/sh',
            '%s',
            'echo \n\n\n',
            'echo Programa terminado con salida: $?',
            'echo Presione Enter para salir.',
            'read I']
        BASH = [
            '#!/bin/sh',
            'xterm -e bash -c "%s"']
        dash = ''
        for i in DASH:
            dash += i + '\n'
        dash = dash % (direc + '/' + self.ejecutable)
        bash = ''
        for i in BASH:
            bash += i + '\n'
        bash = bash % dash
        if _TUX:
            self.pro = Popen(bash, stdout=PIPE, stderr=PIPE, shell=True)
            #stdout, stderr = self.pro.communicate()
        else:
            self.pro = Popen(direc + '/' + self.ejecutable,
                creationflags=CREATE_NEW_CONSOLE)

    def terminar_proceso(self):
        """ Termina el proceso """
        if not self.pro:
            return
        self.pro.terminate()