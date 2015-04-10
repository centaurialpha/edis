# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.Qsci import QsciLexerCPP
from PyQt4.QtGui import QColor

from src import editor_scheme
from src.core import settings


class Lexer(QsciLexerCPP):

    """ Lexer class """

    def __init__(self, *args, **kwargs):
        super(Lexer, self).__init__(*args, **kwargs)
        # Configuración
        self.setStylePreprocessor(True)
        self.setFoldComments(True)
        self.setFoldPreprocessor(True)
        self.setFoldCompact(False)

        self.load_highlighter()

    def load_highlighter(self):
        """ Método público: carga el resaltado de sintáxis """

        scheme = editor_scheme.get_scheme(
            settings.get_setting('editor/scheme'))
        self.setDefaultPaper(QColor(scheme['BackgroundEditor']))
        self.setPaper(self.defaultPaper(0))
        self.setColor(QColor(scheme['Color']))

        types = dir(self)
        for _type in types:
            if _type in scheme:
                atr = getattr(self, _type)
                self.setColor(QColor(scheme[_type]), atr)
