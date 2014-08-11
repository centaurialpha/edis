#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

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