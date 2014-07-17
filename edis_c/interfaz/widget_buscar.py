#-*- coding: utf-8 -*-

# <Widget encargado de buscar en el editor.>
# This file is part of EDIS-C.

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

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QIcon

#from PyQt4.QtCore import SIGNAL

from edis_c import recursos


class WidgetBuscar(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        #self.parent = parent

        layoutH = QHBoxLayout(self)
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setMargin(0)

        self.lineText = QLineEdit()
        self.lineText.setMaximumWidth(200)
        #self.lineText.setAlignment(Qt.AlignRight)
        self.boton_buscar = QPushButton(QIcon(
            recursos.ICONOS['buscar']), '')
        self.boton_anterior = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowLeft), '')
        self.boton_siguiente = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowRight), '')

        layoutH.addWidget(self.boton_buscar)
        layoutH.addWidget(self.lineText)
        layoutH.addWidget(self.boton_anterior)
        layoutH.addWidget(self.boton_siguiente)

        #self.connect(self.boton_buscar, SIGNAL("clicked()"),
         #   self.buscar_texto)