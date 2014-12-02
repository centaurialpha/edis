# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QFontMetrics,
    QColor,
    #QFont
    )

from PyQt4.QtCore import (
    Qt,
    )

from PyQt4.Qsci import (
    QsciScintilla
    )

from src.helpers import configuraciones
from src.ui.editor import lexer


class Base(QsciScintilla):

    def __init__(self):
        super(Base, self).__init__()
        # Configuración de Qscintilla
        self.setCaretLineVisible(True)
        self.setIndentationsUseTabs(False)
        #FIXME: indentación, guías
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.__indentacion = configuraciones.INDENTACION
        self.setIndentationWidth(self.__indentacion)

        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE,
                            QsciScintilla.CARETSTYLE_BLOCK)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        # Indicador
        self.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, 0,
                            QsciScintilla.INDIC_ROUNDBOX)
        self.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 0, 0x0000ff)

        # Folding
        self.setFolding(QsciScintilla.BoxedFoldStyle)

        self.__fuente = None
        self._nombre = ""
        self.cargar_signals()

    def cargar_signals(self):
        """ Carga señales del editor """

        self.linesChanged.connect(self.actualizar_sidebar)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, _nombre):
        self._nombre = _nombre
        if _nombre:
            self.nuevo_archivo = False

    @property
    def texto(self):
        """ Devuelve el texto del documento """

        return self.text()

    @texto.setter
    def texto(self, texto):
        """ Setea el texto en el documento """

        self.setText(texto)

    @property
    def lineas(self):
        """ Devuelve la cantidad de líneas """

        return self.lines()

    @property
    def modificado(self):
        """ True si el documento ha sido modificado """

        return self.isModified()

    def zoom_in(self):
        self.zoomIn()

    def zoom_out(self):
        self.zoomOut()

    def cargar_fuente(self, fuente):
        self.__fuente = fuente
        self.setFont(fuente)
        self.setMarginsFont(fuente)
        self.setMarginLineNumbers(0, True)

    def actualizar_sidebar(self):
        """ Ajusta el ancho del sidebar """

        fmetrics = QFontMetrics(self.__fuente)
        lineas = str(self.lineas) + '00'

        if len(lineas) != 1:
            ancho = fmetrics.width(lineas)
            self.setMarginWidth(0, ancho)

    def match_braces(self, match=None):
        if match:
            self.setBraceMatching(match)

    def match_braces_color(self, fondo, fore):
        self.setMatchedBraceBackgroundColor(QColor(fondo))
        self.setMatchedBraceForegroundColor(QColor(fore))

    def unmatch_braces_color(self, fondo, fore):
        self.setUnmatchedBraceBackgroundColor(QColor(fondo))
        self.setUnmatchedBraceForegroundColor(QColor(fore))

    def caret_line(self, fondo, fore, opacidad):
        color = QColor(fondo)
        color.setAlpha(opacidad)
        self.setCaretForegroundColor(QColor(fore))
        self.setCaretLineBackgroundColor(QColor(color))

    def set_lexer(self, ext):
        if ext == 'cpp':
            self.__lexer = lexer.LexerC(self)
            self.setLexer(self.__lexer)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.delta() > 0:
                self.zoom_in()
            elif e.delta() < 0:
                self.zoom_out()
            e.ignore()
        super(Base, self).wheelEvent(e)