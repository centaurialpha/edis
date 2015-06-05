# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
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

    def keywords(self, kset):
        super(Lexer, self).keywords(kset)
        if kset == 1:
            # Palabras reservadas
            return ('auto break case const continue default do else enum '
                    'extern for goto if register return short sizeof static '
                    'struct switch typedef union unsigned void volatile while '
                    'char float int long double')
        elif kset == 2:
            # Funciones definidas en stdio.h y stdlib.h
            return ('fprintf fscanf printf scanf sprintf sscanf vfprintf '
                    'vprintf vsprintf fclose fflush fopen freopen remove '
                    'rename setbuf tmpfile tmpnam fgetc fgets fputc fputs '
                    'getc getchar gets putc putchar puts ungetc fread fseek '
                    'fsetpos ftell rewind clearerr feof ferror perror '
                    'abort atexit exit getenv system abs div labs ldiv '
                    'rand srand atof atoi atol strtod strtod strtoll '
                    'strtoul bsearch qsort calloc realloc malloc free '
                    'mblen mbtowc wctomb mbstowcs wcstombs')
        super(Lexer, self).keywords(kset)