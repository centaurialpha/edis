# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QGraphicsOpacityEffect

from PyQt4.Qsci import QsciScintilla


class Minimap(QsciScintilla):

    def __init__(self, weditor):
        QsciScintilla.__init__(self, weditor)
        self._weditor = weditor
        self._indentation = self._weditor.indentation
        self.setLexer(self._weditor.lexer())
        # Configuración Scintilla
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.SendScintilla(QsciScintilla.SCI_HIDESELECTION, True)
        self.setFolding(QsciScintilla.NoFoldStyle, 1)
        self.setReadOnly(True)
        self.setCaretWidth(0)
        self.setStyleSheet("background: transparent; border: 0px;")
        # Opacity
        self.efect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efect)
        self.efect.setOpacity(0.5)

    def update_geometry(self):
        editor_width = self._weditor.width()
        height = self._weditor.height()
        width = editor_width * 0.173
        self.setFixedSize(width, height)
        self.move(editor_width - self.width(), 0)
        self.zoomTo(-10)

    def update_code(self):
        text = self._weditor.text().replace('\t', ' ' * self._indentation)
        self.setText(text)