# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.Qsci import QsciLexerCPP
from PyQt4.QtGui import *


class LexerC(QsciLexerCPP):

    def __init__(self, parent):
        QsciLexerCPP.__init__(self, parent)
        self.setStylePreprocessor(True)
        self.setHighlightHashQuotedStrings(True)
        self.lexer = Lexer()
        #FIXME: fuente
        #FIXME: tema


class Lexer:

    def __init__(self, lenguaje='cpp'):
        self.__lenguaje = lenguaje

    @property
    def lenguaje(self):
        return self.__lenguaje

    @lenguaje.setter
    def lenguaje(self, leng):
        if leng != 'cpp':
            self.__lenguaje = None