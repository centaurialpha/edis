# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QFontMetrics,
    QColor,
    )

from PyQt4.QtCore import (
    Qt,
    )

from PyQt4.Qsci import (
    QsciScintilla
    )

from src import recursos
from src.helpers import settings


class Base(QsciScintilla):

    """ Esta clase reimplementa métodos de QsciScintilla y configura atributos.

    La clase Editor está basada en ésta clase.

    """

    def __init__(self):
        QsciScintilla.__init__(self)
        # Configuración de Qscintilla
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(settings.get_setting('editor/indent'))
        self.setBackspaceUnindents(True)
        # Scrollbar
        self.send("sci_sethscrollbar", 0)
        # Indicadores
        self._word_indicator = 0
        self._warning_indicator = 1
        self._error_indicator = 2
        # Estilo de indicadores
        self.send("sci_indicsetstyle", self._word_indicator, "indic_box")
        self.send("sci_indicsetfore", self._word_indicator,
            QColor("#ccd900"))
        self.send("sci_indicsetstyle", self._warning_indicator, "indic_dots")
        self.send("sci_indicsetfore", self._warning_indicator,
            QColor("#ffff00"))
        self.send("sci_indicsetstyle", self._error_indicator, "indic_dots")

        # Folding
        self.setFolding(1)
        self.colorFoldMargen(recursos.TEMA['FoldMarginBack'],
                             recursos.TEMA['FoldMarginFore'])

        self._fuente = None

        self.linesChanged.connect(self.actualizar_sidebar)

    @property
    def texto(self):
        """ Devuelve el texto del documento """

        return self.text()

    @texto.setter
    def texto(self, texto):  # lint:ok
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
        self.send("sci_zoomin")

    def zoom_out(self):
        self.send("sci_zoomout")

    def actualizar_sidebar(self):
        """ Ajusta el ancho del sidebar """

        fmetrics = QFontMetrics(self._fuente)
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

    def send(self, *args):
        """
        Éste método es una reimplementación de SendScintilla.

        Argumento *args:
        args es una tupla, cada elemento es un argumento que será enviado
        como mensaje a QsciSintilla.

        """

        return self.SendScintilla(*[
            getattr(self, arg.upper()) if isinstance(arg, str)
            else arg
            for arg in args])

    def clear_indicators(self, indicador):
        """ Elimina todos los indicadores @indicador """

        self.clearIndicatorRange(0, 0, self.lineas, 0, indicador)

    def colorFoldMargen(self, fore, fondo):
        self.setFoldMarginColors(QColor(fore), QColor(fondo))

    def wheelEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.delta() > 0:
                self.zoom_in()
            elif e.delta() < 0:
                self.zoom_out()
            e.ignore()
        super(Base, self).wheelEvent(e)