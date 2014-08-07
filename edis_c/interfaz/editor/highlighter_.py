#-*- coding: utf-8 -*-

# Basado en Python Syntax highlighting de:
# https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting

from PyQt4.QtGui import QColor
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QBrush

from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.interfaz.editor import sintaxis


def formato(color, estilo=''):
    """ Retorna un QTextCharformat con atributos dados. """

    color_ = QColor()
    color_.setNamedColor(color)

    formato_ = QTextCharFormat()
    formato_.setForeground(color_)

    if 'bold' in estilo:
        formato_.setFontWeight(QFont.Bold)
    if 'italic' in estilo:
        formato_.setFontItalic(True)

    return formato_

# Estilos de sintaxis
ESTILOS = {}
    #'palabra': formato('blue', 'bold'),
    #'operador': formato('red'),
    #'brace': formato('darkGray'),
    #'struct': formato('black', 'bold'),
    #'cadena': formato('magenta'),
    #'caracter': formato('cyan'),
    #'include': formato('darkBlue'),
    #'comentario': formato('darkGreen', 'italic'),
    #'numero': formato('brown')
#}


def re_estilo(tema):
    ESTILOS['palabra'] = formato(tema.get('palabra',
        recursos.TEMA_EDITOR['palabra']), 'bold')
    ESTILOS['operador'] = formato(tema.get('operador',
        recursos.TEMA_EDITOR['operador']))
    ESTILOS['brace'] = formato(tema.get('brace',
        recursos.TEMA_EDITOR['brace']))
    ESTILOS['struct'] = formato(tema.get('struct',
        recursos.TEMA_EDITOR['struct']), 'bold')
    ESTILOS['cadena'] = formato(tema.get('cadena',
        recursos.TEMA_EDITOR['cadena']))
    ESTILOS['caracter'] = formato(tema.get('caracter',
        recursos.TEMA_EDITOR['caracter']))
    ESTILOS['include'] = formato(tema.get('include',
        recursos.TEMA_EDITOR['include']))
    ESTILOS['comentario'] = formato(tema.get('comentario',
        recursos.TEMA_EDITOR['comentario']), 'italic')
    ESTILOS['numero'] = formato(tema.get('numero',
        recursos.TEMA_EDITOR['numero']))


class Highlighter(QSyntaxHighlighter):
    """ Highlighter EDIS-C. """

    # Tupla palabras reservadas de C
    palabras_reservadas = sintaxis.palabras_reservadas

    # Operadores
    operadores = [
        '=',
        '==', '!=', '<', '>', '<=', '>=',
        '\+', '-', '\*', '/', '\%',
        ]

    # Paréntesis, corchetes, llaves
    braces = [
        '\(', '\)',
        '\[', '\]',
        '\{', '\}'
        ]

    def __init__(self, documento, tema):
        QSyntaxHighlighter.__init__(self, documento)
        re_estilo(tema)
        # Reglas
        reglas = []
        # Palabras reservadas
        reglas += [(r'\b%s\b' % w, 0, ESTILOS['palabra'])
            for w in Highlighter.palabras_reservadas]
        # Operadores
        reglas += [(r'%s' % o, 0, ESTILOS['operador'])
            for o in Highlighter.operadores]
        # Braces
        reglas += [(r'%s' % b, 0, ESTILOS['brace'])
            for b in Highlighter.braces]
        # Struct
        reglas += [(r'\bstruct\b\s*(\w+)', 1, ESTILOS['struct'])]
        # Caracter
        reglas += [(r"'[^'\\]*(\\.[^'\\]*)*'", 0, ESTILOS['caracter'])]
        # Numeros
        reglas += [(r'\b[+-]?[0-9]+[lL]?\b', 0, ESTILOS['numero']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, ESTILOS['numero']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b',
                0, ESTILOS['numero'])]
        # Cadena
        reglas += [(r'"[^"\\]*(\\.[^"\\]*)*"', 0, ESTILOS['cadena'])]
        # Include
        reglas += [(r'#[^\n]*', 0, ESTILOS['include'])]
        # Comentario simple
        reglas += [(r'//[^\n]*', 0, ESTILOS['comentario'])]
        # Comentario múltiple
        self.comentario_multiple_lineas = QTextCharFormat()
        color = QColor(200, 0, 10)
        brush = QBrush(color, Qt.SolidPattern)
        self.comentario_multiple_lineas.setForeground(brush)
        self.comentario_inicio = QRegExp("/\\*")
        self.comentario_final = QRegExp("\\*/")

        self.reglas = [(QRegExp(pat), indice, fmt)
            for (pat, indice, fmt) in reglas]
        self.rehighlight()

    def highlightBlock(self, texto):

        for expresion, nth, formato in self.reglas:
            indice = expresion.indexIn(texto, 0)

            while indice >= 0:
                indice = expresion.pos(nth)
                length = expresion.cap(nth).length()
                self.setFormat(indice, length, formato)
                indice = expresion.indexIn(texto, indice + length)

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