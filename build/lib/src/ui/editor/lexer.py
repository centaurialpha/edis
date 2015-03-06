# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.Qsci import QsciLexerCPP
from PyQt4.QtGui import QColor

from src import recursos


class Lexer(QsciLexerCPP):

    """ Lexer para C """

    def __init__(self, *args, **kwargs):
        super(Lexer, self).__init__(*args, **kwargs)
        # Configuración
        self.setStylePreprocessor(True)
        self.setFoldComments(True)
        self.setFoldPreprocessor(True)
        self.setFoldCompact(False)

        self._load_highlighter()

    def _load_highlighter(self):
        """ Método privado que carga el resaltado de sintáxis """

        self.setDefaultPaper(QColor(recursos.TEMA['FondoEditor']))
        self.setPaper(self.defaultPaper(0))
        self.setColor(QColor(recursos.TEMA['Color']))

        types = dir(self)
        for _type in types:
            if _type in recursos.TEMA:
                atr = getattr(self, _type)
                self.setColor(QColor(recursos.TEMA[_type]), atr)