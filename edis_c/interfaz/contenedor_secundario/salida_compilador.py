#-*- coding: utf-8 -*-

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

# Módulos QtGui
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QMenu

# Módulos QtCore
from PyQt4.QtCore import Qt


class SalidaWidget(QPlainTextEdit):
    """ Clase QPlainTextEdit para la salida del compilador. """

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self._parent = parent
        self.setReadOnly(True)

        # Formato para la salida estándar
        self.formato_ok = QTextCharFormat()
        # Formato para la salida de error
        self.formato_error = QTextCharFormat()
        self.formato_error.setAnchor(True)
        self.formato_error.setFontUnderline(True)
        self.formato_error.setUnderlineColor(Qt.red)
        self.formato_error.setUnderlineStyle(QTextCharFormat.DashDotLine)
        self.formato_error.setFontPointSize(10)
        self.formato_error.setForeground(Qt.darkRed)
        # Formato para la salida de error (warnings)
        self.formato_warning = QTextCharFormat()
        self.formato_warning.setAnchor(True)
        self.formato_warning.setFontUnderline(True)
        self.formato_warning.setUnderlineColor(Qt.yellow)
        self.formato_warning.setUnderlineStyle(QTextCharFormat.DotLine)
        self.formato_warning.setFontPointSize(9)
        self.formato_warning.setForeground(Qt.darkYellow)

        # Se carga el estilo
        self.cargar_estilo()

    def cargar_estilo(self):
        """ Carga estilo de color de QPlainTextEdit """

        tema = 'QPlainTextEdit {color: #333; background-color: #f6f6f6;}' \
        'selection-color: #FFFFFF; selection-background-color: #009B00;'

        self.setStyleSheet(tema)

    def contextMenuEvent(self, evento):
        """ Context menú """

        menu = self.createStandardContextMenu()

        menuSalida = QMenu(self.trUtf8("Salida"))
        limpiar = menuSalida.addAction(self.trUtf8("Limpiar"))
        menu.insertSeparator(menu.actions()[0])
        menu.insertMenu(menu.actions()[0], menuSalida)

        limpiar.triggered.connect(lambda: self.setPlainText('\n\n'))

        menu.exec_(evento.globalPos())

    def salida_estandar(self):
        """ Muestra la salida estándar. """

        cp = self._parent.proceso
        text = cp.readAllStandardOutput().data()
        self.textCursor().insertText(text, self.formato_ok)

    def parser_salida_stderr(self):
        """ Parser de la salida stderr """
        # FIXME
        codificacion = 'utf-8'
        cursor = self.textCursor()
        proceso = self._parent.proceso
        texto = proceso.readAllStandardError().data().decode(codificacion)
        lineas = texto.split('\n')
        lista = []
        for l in lineas:
            if l:
                lista.append(l.strip())

        for t in lista:
            for i in t.split(':'):
                if i.strip() == 'error':
                    cursor.insertText(t, self.formato_error)
                    cursor.insertText('\n')
                elif i.strip() == 'warning':
                    cursor.insertText(t, self.formato_warning)
                    cursor.insertText('\n')
        cursor.insertText('\n')
        cursor.insertText(lista[-1], self.formato_ok)  # E y W generados

    def parsear_string(self, cadena):
        pass

    def datos_tabla(self):
        pass

    def errores_advertencias(self, errores, warnings):
        # TODO: mostrar cantidad de errores y línea
        pass

    def setFoco(self):
        self.setFocus()