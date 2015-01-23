# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTextCursor

# Módulos QtCore
from PyQt4.QtCore import Qt


class DialogoInsertarInclude(QDialog):

    def __init__(self, weditor, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.trUtf8('Insertar include'))
        self.weditor = weditor

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(self.trUtf8("#include")))
        self.line_include = QLineEdit()
        layout.addWidget(self.line_include)
        self.boton_agregar = QPushButton(self.trUtf8("Insertar"))
        layout.addWidget(self.boton_agregar)

        self.line_include.returnPressed.connect(self.agregar_include)
        self.boton_agregar.clicked.connect(self.agregar_include)

    def agregar_include(self):
        texto = self.line_include.text()
        cursor = self.weditor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.EndOfLine)
        include = '\n#include <{0}.h>'.format(texto)
        if self.weditor.document().find(
            include[1:]).position() == -1:
                cursor.insertText(include)
        self.close()