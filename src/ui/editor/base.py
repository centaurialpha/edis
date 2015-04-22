# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtCore import Qt

from PyQt4.Qsci import (
    QsciScintilla
    )


class Base(QsciScintilla):

    """ Base Editor """

    def __init__(self):
        QsciScintilla.__init__(self)

    def zoom_in(self):
        self.send("sci_zoomin")

    def zoom_out(self):
        self.send("sci_zoomout")

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

    def clear_indicators(self, indicator):
        """ Elimina todos los indicadores @indicador """

        self.clearIndicatorRange(0, 0, self.lines(), 0, indicator)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.delta() > 0:
                self.zoom_in()
            elif e.delta() < 0:
                self.zoom_out()
            e.ignore()
        super(Base, self).wheelEvent(e)
