"""
<syntax.py - Modulo con las funciones para el resaltado de sintaxis.>
Copyright (C) <2014>  <Dario Gabriel Acosta>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.Qt import QTextCharFormat
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtCore import *

from sintaxis import palabras_reservadas


class Sintaxis(QSyntaxHighlighter):
    def __init__(self, parent, theme):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        palabraClave = QTextCharFormat()
        #funcionClave = QTextCharFormat()
        delimitador = QTextCharFormat()
        comentario = QTextCharFormat()
        comentario_2 = QTextCharFormat()
        include = QTextCharFormat()
        punto_coma = QTextCharFormat()
        cabecera = QTextCharFormat()
        numeros = QTextCharFormat()
        texto_en_comillas = QTextCharFormat()

        self.highlightingRules = []

        # Palabras Reservadas
        color = QColor(31, 192, 232)
        brush = QBrush(color, Qt.SolidPattern)
        palabraClave.setForeground(brush)
        palabraClave.setFontWeight(QFont.Bold)
        palabrasClaves = QStringList(palabras_reservadas)

        for palabra in palabrasClaves:
            patron = QRegExp("\\b" + palabra + "\\b")
            regla = HighlightingRule(patron, palabraClave)
            self.highlightingRules.append(regla)

        #color = QColor(230, 219, 116)
        #brush = QBrush(color, Qt.SolidPattern)
        #funcionClave.setForeground(brush)
        ##funcionClave.setFontWeight(QFont.Bold)
        #funcionesClaves = QStringList(funciones_reservadas)

        #for palabra in funcionesClaves:
            #patron = QRegExp("\\b" + palabra + "\\b")
            #regla = HighlightingRule(patron, funcionClave)
            #self.highlightingRules.append(regla)

        # Delimitadores
        patron = QRegExp("[\)\(]+|[\{\}]+|[][]+")
        Color = QColor(255, 255, 255)
        color = QBrush(Color, Qt.SolidPattern)
        delimitador.setForeground(color)
        delimitador.setFontWeight(QFont.Bold)
        regla = HighlightingRule(patron, delimitador)
        self.highlightingRules.append(regla)

        # Comentarios //
        color = QColor(170, 170, 170)
        brush = QBrush(color, Qt.SolidPattern)
        patron = QRegExp("//[^\n]*")
        comentario.setForeground(brush)
        regla = HighlightingRule(patron, comentario)
        self.highlightingRules.append(regla)

        # Comentarios /* */
        #FIXME: No funciona por ahora, solo comenta en una linea
        color = QColor(210, 170, 0)
        brush = QBrush(color, Qt.SolidPattern)
        patron = QRegExp("\/*.*\*/")
        comentario_2.setForeground(brush)
        regla = HighlightingRule(patron, comentario_2)
        self.highlightingRules.append(regla)

        # Includes
        color = QColor(80, 135, 8)
        brush = QBrush(color, Qt.SolidPattern)
        patron = QRegExp("#[^\n]*")
        include.setForeground(brush)
        include.setFontWeight(QFont.Bold)
        regla = HighlightingRule(patron, include)
        self.highlightingRules.append(regla)

        # Punto y coma
        color = QColor(255, 255, 255)
        brush = QBrush(color, Qt.SolidPattern)
        patron = QRegExp(";")
        punto_coma.setForeground(brush)
        regla = HighlightingRule(patron, punto_coma)
        self.highlightingRules.append(regla)

        # Cabeceras
        color = QColor(231, 106, 14)
        brush = QBrush(color, Qt.SolidPattern)
        patron = QRegExp("\<.*\>")
        cabecera.setForeground(brush)
        regla = HighlightingRule(patron, cabecera)
        self.highlightingRules.append(regla)

        # Numeros
        patron = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
        color = QColor(130, 180, 0)
        patron.setMinimal(True)
        numeros.setForeground(color)
        regla = HighlightingRule(patron, numeros)
        self.highlightingRules.append(regla)

        # Texto en comillas
        color = QColor(240, 180, 0)
        brush = QBrush(color, Qt.SolidPattern)
        fuente = QFont("Clasicc", 9, QFont.Bold, False)
        patron = QRegExp("\".*\"")
        texto_en_comillas.setForeground(brush)
        texto_en_comillas.setFont(fuente)
        regla = HighlightingRule(patron, texto_en_comillas)
        self.highlightingRules.append(regla)

    def highlightBlock(self, text):
        for regla in self.highlightingRules:
            expresion = QRegExp(regla.patron)
            index = expresion.indexIn(text)
            while index >= 0:
                length = expresion.matchedLength()
                self.setFormat(index, length, regla.format)
                index = text.indexOf(expresion, index + length)
        self.setCurrentBlockState(0)


class HighlightingRule():

    def __init__(self, patron, format):
        self.patron = patron
        self.format = format
