#-*- coding: utf-8 -*-

from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor

from PyQt4.Qt import QTextCharFormat

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRegExp

from side_c.gui.editor.sintaxis import palabras_reservadas
from side_c import recursos


class Highlighter(QSyntaxHighlighter):
    """ Highlighter.

    -Comentario simple.
    -Comentario múltiple.
    -Include. ----------> Arreglar
    -Números.
    -Operadores. -------> Arreglar
    -Formateo.
    -Funciones.
    """
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        formato_palabra = QTextCharFormat()
        formato_palabra.setForeground(recursos.HIGHLIGHTER['palabra'])
        formato_palabra.setFontWeight(QFont.Bold)
        patron_palabras = palabras_reservadas
        self.highlightingRules = [(QRegExp(indice), formato_palabra)
        for indice in patron_palabras]

        formato_clase = QTextCharFormat()
        formato_clase.setFontWeight(QFont.Bold)
        formato_clase.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
            formato_clase))

        comentario_una_linea = QTextCharFormat()
        comentario_una_linea.setForeground(
            recursos.HIGHLIGHTER['comentario-simple'])
        self.highlightingRules.append((QRegExp("//[^\n]*"),
            comentario_una_linea))

        include = QTextCharFormat()
        include.setForeground(recursos.HIGHLIGHTER['include'])
        self.highlightingRules.append((QRegExp("#[^\n]*"),
            include))

        struct = QTextCharFormat()
        struct.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("struct[^\n]*"),
            struct))

        numeros = QTextCharFormat()
        numeros.setForeground(recursos.HIGHLIGHTER['numero'])
        self.highlightingRules.append((QRegExp("\\b[0-9]+\\b"),
            numeros))

        self.comentario_multiple_lineas = QTextCharFormat()
        self.comentario_multiple_lineas.setForeground(
            recursos.HIGHLIGHTER['comentario-multiple'])

        operadores = QTextCharFormat()
        color = QColor(200, 200, 200)
        operadores.setForeground(color)
        self.highlightingRules.append((QRegExp("\\b=\\b"),
        operadores))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(recursos.HIGHLIGHTER['cadena'])
        self.highlightingRules.append((QRegExp("\".*\""),
            quotationFormat))

        formateo = QTextCharFormat()
        formateo.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("%[^' ']"),
            formateo))

        funciones = QTextCharFormat()
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
