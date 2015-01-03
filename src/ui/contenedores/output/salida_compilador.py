# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

# Módulos QtGui
from PyQt4.QtGui import (
    QPlainTextEdit,
    QFont,
    QTextCharFormat,
    QMenu
    )

# Módulos QtCore
from PyQt4.QtCore import (
    Qt,
    SIGNAL
    )


class SalidaWidget(QPlainTextEdit):
    """ Clase QPlainTextEdit para la salida del compilador. """

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self.setObjectName("output")
        self._parent = parent
        self.setReadOnly(True)
        # Formato para la salida estándar
        self.formato_ok = QTextCharFormat()
        #self.formato_ok.setAnchor(True)
        self.formato_ok.setFontPointSize(10)
        # Shap
        self.format_shap = QTextCharFormat()
        self.format_shap.setFontWeight(QFont.Bold)
        self.format_shap.setFontPointSize(16)
        self.format_shap.setForeground(Qt.darkGreen)
        # Formato para la salida de error
        self.format_line_error = QTextCharFormat()
        self.format_line_error.setAnchor(True)
        self.format_line_error.setUnderlineColor(Qt.red)
        self.format_line_error.setUnderlineStyle(1)
        self.formato_error = QTextCharFormat()
        self.formato_error.setFontFixedPitch(True)
        self.formato_error.setToolTip(self.trUtf8("Click para ir a la línea"))
        self.formato_error.setAnchor(True)
        self.formato_error.setFontPointSize(9)
        self.formato_error.setForeground(Qt.white)
        self.formato_error.setBackground(Qt.red)
        # Formato para la salida de error (warnings)
        self.formato_warning = QTextCharFormat()
        self.formato_warning.setAnchor(True)
        self.formato_warning.setBackground(Qt.yellow)
        self.formato_warning.setFontPointSize(9)

        # Se carga el estilo
        #self.cargar_estilo()

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

    def mousePressEvent(self, event):
        QPlainTextEdit.mousePressEvent(self, event)
        self.go_to_line(event)

    def go_to_line(self, event):
        text = self.cursorForPosition(event.pos()).block().text()
        line = self.parse_error(text)
        if line:
            self.emit(SIGNAL("irALinea(int)"), int(line))

    def parser_salida_stderr(self):
        """ Parser de la salida stderr """

        espacio = re.compile('^\s+')
        cursor = self.textCursor()
        proceso = self._parent.proceso_compilacion
        texto = proceso.readAllStandardError().data().decode('utf-8')

        for l in texto.splitlines():
            cursor.insertBlock()
            if l.find('warning') != -1:
                cursor.insertText(l, self.formato_warning)
            elif l.find('error') != -1:
                cursor.insertText(l, self.formato_error)
            elif l.find('^') == -1:
                if espacio.match(l):
                    cursor.insertText(l, self.format_line_error)
            else:
                cursor.insertText(l, self.format_shap)

    def parse_error(self, line):
        """ Parse line and return the number line"""

        for e, l in enumerate(line.split(':')):
            if e == 1 and str(l).isdigit():
                return l
        return False

    def setFoco(self):
        self.setFocus()