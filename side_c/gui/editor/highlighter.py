#-*- coding: utf-8 -*-

from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush

from PyQt4.Qt import QTextCharFormat

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRegExp

from side_c.gui.editor.sintaxis import palabras_reservadas
from side_c import recursos


class Highlighter(QSyntaxHighlighter):
    """ Highlighter.

    -Palabras reservadas.
    -Comentario simple.
    -Include. #
    -Include. <>
    -Struct ------------> Arreglar
    -Números.
    -Comentario múltiple.
    -Braces.
    -Caracter.
    -Cadena
    -Caracter especial
    -Formateo.
    -Funciones.
    """
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)

        palabra_clave = QTextCharFormat()
        comentario_una_linea = QTextCharFormat()
        include = QTextCharFormat()
        _include = QTextCharFormat()
        struct = QTextCharFormat()
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
        self.highlightingRules = [(QRegExp(indice + ' '), palabra_clave)
        for indice in palabras_claves]

        # Comentario simple
        comentario_una_linea.setForeground(
            recursos.HIGHLIGHTER['comentario-simple'])
        self.highlightingRules.append((QRegExp("//[^\n]*"),
            comentario_una_linea))

        # Include
        include.setFontItalic(True)
        include.setForeground(recursos.HIGHLIGHTER['include'])
        self.highlightingRules.append((QRegExp("#[^\n]*"),
            include))

        _include.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\<.*\>"), _include))

        # Struct
        struct.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp(" "),
            struct))

        # Numero
        numeros.setFontWeight(QFont.Bold)
        numeros.setForeground(recursos.HIGHLIGHTER['numero'])
        self.highlightingRules.append((QRegExp("\\b[0-9]+\\b"),
            numeros))

        # Comentario múltiple
        self.comentario_multiple_lineas.setForeground(
            recursos.HIGHLIGHTER['comentario-multiple'])

        # Corchete - paréntesis - llave
        braces.setForeground(recursos.HIGHLIGHTER['braces'])
        self.highlightingRules.append((QRegExp("[\[\]\(\)\{\}]"),
        braces))

        # Caracter ''
        caracter.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("\'.*\'"), caracter))

        # Cadena
        cadena.setForeground(recursos.HIGHLIGHTER['cadena'])
        self.highlightingRules.append((QRegExp("\".*\""),
            cadena))

        # Caracter especial
        caracter_especial.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("\\\[a-z]"), caracter_especial))

        # Formateo
        formateo.setForeground(Qt.darkYellow)
        self.highlightingRules.append((QRegExp("%[^' ']"),
            formateo))

        # Funciones
        funciones.setFontItalic(True)
        funciones.setForeground(recursos.HIGHLIGHTER['funcion'])
        self.highlightingRules.append((QRegExp(
            "\\b[A-Za-z0-9_]+(?=\\()"), funciones))

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
