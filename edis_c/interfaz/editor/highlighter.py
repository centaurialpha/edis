#-*- coding: utf-8 -*-

# <Resaltado de sintaxis para C.>
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

from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush

from PyQt4.Qt import QTextCharFormat

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRegExp

from edis_c.interfaz.editor.sintaxis import palabras_reservadas
from edis_c import recursos


class Highlighter(QSyntaxHighlighter):
    """ Highlighter.

    -Palabras reservadas.
    -Funciones.
    -Braces.
    -Caracter.
    -Cadena
    -Include. #
    -Include. <>
    -Formateo.
    -Números.
    -Comentario simple.
    -Comentario múltiple.
    -Caracter especial
    """
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)

        palabra_clave = QTextCharFormat()
        comentario_una_linea = QTextCharFormat()
        include = QTextCharFormat()
        _include = QTextCharFormat()
        numeros = QTextCharFormat()
        self.comentario_multiple_lineas = QTextCharFormat()
        caracter = QTextCharFormat()
        braces = QTextCharFormat()
        caracter_especial = QTextCharFormat()
        cadena = QTextCharFormat()
        formateo = QTextCharFormat()
        funciones = QTextCharFormat()

        # Palabra reservada
        color = QColor(recursos.HIGHLIGHTER['palabra'])
        brush = QBrush(color, Qt.SolidPattern)
        palabra_clave.setForeground(brush)
        palabra_clave.setFontWeight(QFont.Bold)
        palabras_claves = palabras_reservadas
        self.highlightingRules = [(QRegExp(
            "\\b" + indice + "\\b"), palabra_clave)
        for indice in palabras_claves]

        # Funciones
        funciones.setFontItalic(True)
        funciones.setForeground(recursos.HIGHLIGHTER['funcion'])
        self.highlightingRules.append((QRegExp(
            "\\b[A-Za-z0-9_]+(?=\\()"), funciones))

        # Corchete - paréntesis - llave
        braces.setFontWeight(QFont.Bold)
        braces.setForeground(recursos.HIGHLIGHTER['braces'])
        self.highlightingRules.append((QRegExp("[\[\]\(\)\{\}]"),
        braces))

        # Caracter ''
        caracter.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("\'.*\'"), caracter))

        # Numero
        numeros.setForeground(recursos.HIGHLIGHTER['numero'])
        self.highlightingRules.append((QRegExp(
            "\\b[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"),
            numeros))

        # Cadena
        cadena.setForeground(recursos.HIGHLIGHTER['cadena'])
        self.highlightingRules.append((QRegExp("\".*\""),
            cadena))

        # Include
        include.setFontItalic(True)
        include.setForeground(recursos.HIGHLIGHTER['include'])
        self.highlightingRules.append((QRegExp("#[^\n]*"),
            include))

        _include.setForeground(recursos.HIGHLIGHTER['include_'])
        self.highlightingRules.append((QRegExp("\<.*\>"), _include))

        # Formateo
        formateo.setForeground(Qt.darkYellow)
        self.highlightingRules.append((QRegExp("%[^' ']"),
            formateo))

        # Comentario simple
        comentario_una_linea.setForeground(
            recursos.HIGHLIGHTER['comentario'])
        self.highlightingRules.append((QRegExp("//[^\b]*"),
            comentario_una_linea))

        # Comentario múltiple
        self.comentario_multiple_lineas.setForeground(
            recursos.HIGHLIGHTER['comentario'])

        # Caracter especial
        caracter_especial.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("\\\[a-z]"), caracter_especial))

        self.comentario_inicio = QRegExp("/\\*")
        self.comentario_final = QRegExp("\\*/")

    def highlightBlock(self, texto):
        for patron, format in self.highlightingRules:
            expresion = QRegExp(patron)
            indice = expresion.indexIn(texto)
            while indice >= 0:
                tam = expresion.matchedLength()
                self.setFormat(indice, tam, format)
                indice = expresion.indexIn(texto, indice + tam)
        self.setCurrentBlockState(0)
        inicio_indice = 0
        if self.previousBlockState() != 1:
            inicio_indice = self.comentario_inicio.indexIn(texto)
        while inicio_indice >= 0:
            final_indice = self.comentario_final.indexIn(texto, inicio_indice)
            if final_indice == -1:
                self.setCurrentBlockState(1)
                commentLength = texto.length() - inicio_indice
            else:
                commentLength = final_indice - inicio_indice + \
                self.comentario_final.matchedLength()
            self.setFormat(inicio_indice, commentLength,
                self.comentario_multiple_lineas)
            inicio_indice = self.comentario_final.indexIn(texto,
                inicio_indice + commentLength)


class HighlightingRule():

    def __init__(self, patron, format):
        self.patron = patron
        self.format = format
