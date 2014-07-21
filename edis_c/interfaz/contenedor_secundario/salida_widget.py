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

import time
#import sys
import os

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QFont

from PyQt4.QtCore import QProcess
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.nucleo import manejador_de_archivo


class EjecutarWidget(QWidget):

    def __init__(self):
        super(EjecutarWidget, self).__init__()
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        self.output = SalidaWidget(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Proceso
        self.proceso_actual = None
        self.proceso = QProcess(self)

        # Conexión
        self.connect(self.proceso, SIGNAL("readyReadStandardOutput()"),
            self.output.salida_estandar)
        self.connect(self.proceso, SIGNAL("readyReadStandardError()"),
            self.output.error_estandar)
        self.connect(self.proceso, SIGNAL(
            "finished(int, QProcess::ExitStatus)"), self.ejecucion_terminada)
        self.connect(self.proceso, SIGNAL("error(QProcess::ProcessError)"),
            self.ejecucion_error)

    def correr_compilacion(self, nombre_archivo):
        """ Se corre el comando gcc para la compilación """

        # Dirección del archivo a compilar
        self.nombre_archivo = nombre_archivo
        # Nombre del archivo sin extensión
        self.ejecutable = (self.nombre_archivo.split('/')[-1]).split('.')[0]

        self.output.setCurrentCharFormat(self.output.formato_ok)

        # Para generar el ejecutable en la carpeta del fuente
        directorio_archivo = manejador_de_archivo.devolver_carpeta(
            self.nombre_archivo)
        self.proceso.setWorkingDirectory(directorio_archivo)

        # Parámetros adicionales
        parametros_add = list(str(configuraciones.PARAMETROS).split())
        # Parámetros para el compilador
        parametros_gcc = ['-Wall', '-o']
        self.proceso_actual = self.proceso
        self.output.setPlainText(
            'Compilando archivo: %s\nDirectorio: %s ( %s )\n' %
            (self.nombre_archivo.split('/')[-1], self.nombre_archivo,
                time.ctime()))
        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)
        self.output.textCursor().insertBlock()

        # Comenzar proceso
        self.proceso.start('gcc', parametros_gcc + [self.ejecutable] +
            parametros_add + [self.nombre_archivo])

        #self.output.setCurrentCharFormat(self.output.formato_ok)
        #self.ejecutable = nombre_ejecutable

        #if sys.platform is not configuraciones.LINUX:
            #path = "\"%s\"" % path

        #comando = 'gcc -Wall -o %s %s' % (self.ejecutable, path)
        #self.proceso_actual = self.proceso
        #self.proceso_actual.start(comando)

        #archivo = path.split('/')[-1]
        #self.output.setPlainText(
            #'Compilando archivo:  %s\nDirectorio: %s ( %s )\n' %
            #(archivo, os.path.dirname(path), time.ctime()))
        #self.output.moveCursor(QTextCursor.Down)
        #self.output.moveCursor(QTextCursor.Down)

    def ejecucion_terminada(self, codigoError, exitStatus):
        """ valores de codigoError
            0 = Cuando se compila bien, aún con advertencias
            1 = Error en la compilación
        """
        formato = QTextCharFormat()
        formato.setAnchor(True)
        formato.setFontWeight(QFont.Bold)
        formato.setFontPointSize(11)

        self.output.textCursor().insertText('\n\n')
        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(
                QBrush(QColor(recursos.COLOR_EDITOR['salida-exitosa'])))
            self.output.textCursor().insertText(
                self.trUtf8("¡Compilación exitosa!"), formato)

        else:
            formato.setForeground(
                QBrush(QColor(recursos.COLOR_EDITOR['salida-error'])))
            self.output.textCursor().insertText(
                self.trUtf8("No hubo compilación!"), formato)
        self.output.textCursor().insertText('\n')
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_error(self, error):
        pass

    def correr_programa(self):
        """ Se encarga de correr el programa ejecutable.
        Arreglar: Para que corra el programa con QProcess y además que borre
        el código de salida anterior con (rm $0).
        """
        direc = manejador_de_archivo.devolver_carpeta(self.nombre_archivo)
        #ejecutar = "./"
        dash = """
        #!/bin/sh
        %s
        echo \n\n\n
        echo '------------------------------'
        echo 'Presione <Enter> para salir'
        read variable_al_pp
        """ % (direc + '/' + self.ejecutable)
        bash = """
        #!/bin/sh
        xterm -e bash -c "%s"
        """ % dash
        #self.proceso_actual = self.proceso_ejecucion

        #comando = 'xterm -e bash -c ./%s'
        #self.proceso_actual.start(bash)
        os.popen(bash)


class SalidaWidget(QPlainTextEdit):

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self._parent = parent
        self.setReadOnly(True)

        # Formato para la salida estándar
        self.formato_ok = QTextCharFormat()
        #self.formato_ok.setForeground(recursos.COLOR_EDITOR['texto'])

        # Formato para la salida de error
        self.formato_error = QTextCharFormat()
        self.formato_error.setAnchor(True)
        self.formato_error.setFontUnderline(True)
        self.formato_error.setUnderlineColor(Qt.red)
        self.formato_error.setForeground(Qt.blue)

        # Se carga el estilo
        self.cargar_estilo()

    def cargar_estilo(self):
        """ Carga estilo de color de QPlainTextEdit """

        tema = 'QPlainTextEdit {color: #333; background-color: #ffffff;}' \
        'selection-color: #FFFFFF; selection-background-color: #009B00;'

        self.setStyleSheet(tema)

    def salida_estandar(self):

        cp = self._parent.proceso
        text = cp.readAllStandardOutput().data()
        self.textCursor().insertText(text, self.formato_error)

    def error_estandar(self):

        codificacion = 'utf-8'
        cursor = self.textCursor()
        proceso = self._parent.proceso
        texto = proceso.readAllStandardError().data().decode(codificacion)
        cursor.insertText(texto, self.formato_error)