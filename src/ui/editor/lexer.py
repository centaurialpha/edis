# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.Qsci import QsciLexerCPP
from PyQt4.QtGui import (
    QFont,
    )

from src.helpers import configuraciones


class LexerC(QsciLexerCPP):

    def __init__(self, parent):
        QsciLexerCPP.__init__(self, parent)
        self.setStylePreprocessor(True)
        self.setHighlightHashQuotedStrings(True)
        self.lexer = Lexer()
        self.setFont(self.lexer.fuente)
        #FIXME: tema


class Lexer:

    @property
    def fuente(self):
        fuente = QFont()
        fuente.setFamily(configuraciones.FUENTE)
        fuente.setPointSize(configuraciones.TAM_FUENTE)
        return fuente