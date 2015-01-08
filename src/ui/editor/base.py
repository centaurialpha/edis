# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
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

from src import recursos
from src.helpers import configuracion


class Base(QsciScintilla):

    """ Esta clase reimplementa métodos de QsciScintilla y configura atributos.

    La clase Editor está basada en ésta clase.

    """

    def __init__(self):
        QsciScintilla.__init__(self)
        # Configuración de Qscintilla
        self.esettings = configuracion.ESettings()
        self.setCaretLineVisible(self.esettings.get('editor/margen'))
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        # Cursor
        self.send("sci_setcaretstyle", "caretstyle_block")
        # Scrollbar
        self.send("sci_sethscrollbar", 0)
        # Indicadores
        self.indicador = 0
        self.indicador_warning = 1
        self.indicador_error = 2
        self.send("sci_indicsetstyle", self.indicador, "indic_container")
        self.send("sci_indicsetalpha", self.indicador, 100)
        self.send("sci_indicsetfore", self.indicador, 0x0000ff)
        self.send("sci_indicsetstyle", self.indicador_warning, "indic_dots")
        self.send("sci_indicsetfore", self.indicador_warning, QColor('yellow'))
        self.send("sci_indicsetstyle", self.indicador_error, "indic_dots")
        self.send("sci_indicsetfore", self.indicador_error, 0x0000ff)

        # Folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.colorFoldMargen(recursos.TEMA['foldFore'],
                            recursos.TEMA['foldBack'])

        self.__fuente = None

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
        self.send("zoomin")

    def zoom_out(self):
        self.send("zoomout")

    def deshacer(self):
        self.send("undo")

    def rehacer(self):
        self.send("redo")

    def cortar(self):
        self.send("cut")

    def copiar(self):
        self.send("copy")

    def pegar(self):
        self.send("paste")

    def seleccionar(self):
        self.send("selectall")

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

    def borrarIndicadores(self, indicador):
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