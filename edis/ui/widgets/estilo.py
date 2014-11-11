#-*- coding: utf8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

# Módulos QtGui
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel

# Módulos EDIS
from edis.ui import tabitem


class EstiloDeCodigo(QPlainTextEdit, tabitem.TabItem):

    def __init__(self):
        super(EstiloDeCodigo, self).__init__()
        tabitem.TabItem.__init__(self)
        self.setReadOnly(True)
        self.setStyleSheet("color: #666")
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(QLabel(
            self.trUtf8("<h1>Estilos de código para C</h1>")))
        layout.addWidget(QLabel(
            self.trUtf8("Algunas convenciones o estándares para escribir"
            " código en C.")))
        layout.addWidget(QLabel(
            self.trUtf8("<b>Líneas</b><br>Con una sola instrucción por línea"
            " el código quedaría más legible.<br>\twhile")))
        self.setLayout(layout)