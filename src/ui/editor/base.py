#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QFontMetrics,
    QColor,
    )

from PyQt4.QtCore import (
    Qt
    )

from PyQt4.Qsci import (
    QsciScintilla,
    QsciLexerCPP
    )

from src.helpers import configuraciones


class Base(QsciScintilla):

    def __init__(self):
        super(Base, self).__init__()

        # Configuración de Qscintilla
        self.setCaretLineVisible(True)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)

        self.__fuente = None
        self._id = ""

        #FIXME: lexer
        self.lexer = QsciLexerCPP()
        self.setLexer(self.lexer)

        self.cargar_signals()

    def cargar_signals(self):
        """ Carga señales del editor """

        self.linesChanged.connect(self.actualizar_sidebar)

    def get_id(self):
        return self._id

    def set_id(self, id_):
        self._id = id_
        if id_:
            self.nuevo_archivo = False

    iD = property(lambda self: self.get_id(), lambda self,
        nombre: self.set_id(nombre))

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

    def margen_de_linea(self, margen, color):
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(margen)
        self.setEdgeColor(QColor(color))

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

    def wheelEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.delta() > 0:
                self.zoom_in()
            elif e.delta() < 0:
                self.zoom_out()
            e.ignore()
        super(Base, self).wheelEvent(e)