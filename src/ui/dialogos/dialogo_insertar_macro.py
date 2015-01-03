# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTextCursor
from PyQt4.QtCore import Qt


class DialogoInsertarMacro(QDialog):

    def __init__(self, weditor, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.trUtf8("Insertar macro"))
        self.weditor = weditor

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(self.trUtf8("#define")))
        self.line_define = QLineEdit()
        layout.addWidget(self.line_define)
        self.line_valor = QLineEdit()
        self.line_valor.setPlaceholderText(self.trUtf8("valor"))
        layout.addWidget(self.line_valor)
        self.boton_agregar = QPushButton(self.trUtf8("Agregar"))
        layout.addWidget(self.boton_agregar)

        self.boton_agregar.clicked.connect(self.agregar_macro)

    def agregar_macro(self):
        itemDefine = self.line_define.text()
        itemValor = self.line_valor.text()

        cursor = self.weditor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.EndOfLine)
        macro = '\n#define {0} {1}'.format(itemDefine, itemValor)
        if self.weditor.document().find(
            macro[1:]).position() == -1:
                cursor.insertText(macro)
        self.close()
