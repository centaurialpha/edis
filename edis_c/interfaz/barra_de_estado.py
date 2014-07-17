#-*- coding: utf-8 -*-

# <Barra de estado, muestra statustips y eventos que ocurren en el editor.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

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

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from edis_c import recursos

_instanciaBarraDeEstado = None


def BarraDeEstado(*args, **kw):
    global _instanciaBarraDeEstado
    if _instanciaBarraDeEstado is None:
        _instanciaBarraDeEstado = _BarraDeEstado(*args, **kw)

    return _instanciaBarraDeEstado


class _BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()

        v_layout = QVBoxLayout(self.widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        #v_layout.setSpacing(20)

        self.linea_columna = EstadoLineaColumna(self)
        v_layout.addWidget(self.linea_columna)
        self.connect(self, SIGNAL("messageChanged(QString)"),
            self.mensaje_terminado)

        self.addWidget(self.widget)

    def showMessage(self, mensaje, tiempo):
        self.linea_columna.hide()
        QStatusBar.showMessage(self, mensaje, tiempo)

    def mensaje_terminado(self, mensaje):
        if not mensaje:
            self.linea_columna.show()


class EstadoLineaColumna(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.parent = parent

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        self.texto = "Linea: %s | Columna: %s"
        self.posicion_cursor = QLabel(self.trUtf8(
            self.texto % (0, 0)))

        layoutH.addWidget(self.posicion_cursor)

        layoutV.addLayout(layoutH)

    def actualizar_linea_columna(self, linea, columna):
        self.posicion_cursor.setText(
            self.trUtf8(self.texto % (linea, columna)))