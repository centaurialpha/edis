# -*- coding: utf-8 -*-

# <Agrega el contenedor lateral, central y el output.>
# This file is part of EDIS.

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
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL


class WidgetCentral(QWidget):
    """ Clase contenedora de los widgets. """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.lateral = None
        layout_horizontal = QHBoxLayout(self)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)

        self.split_horizontal = QSplitter(Qt.Horizontal)
        self.split_principal = QSplitter(Qt.Vertical)
        self.layout = QHBoxLayout()

        layout_horizontal.addWidget(self.split_horizontal)
        layout_horizontal.addLayout(self.layout)

    def agregar_contenedor_central(self, contenedor):
        """ Agrega widget principal. """

        self.contenedor_principal = contenedor
        self.split_principal.insertWidget(0, contenedor)

    def agregar_contenedor_lateral(self, explorador):
        self.lateral = Lateral(explorador)
        self.split_horizontal.insertWidget(0, self.lateral)
        self.emit(SIGNAL("lateral()"))

    def agregar_buscador(self, buscador):
        """ Agrega widget de búsqueda. """

        self.buscador = buscador
        self.buscador.hide()
        self.split_principal.insertWidget(1, buscador)

    def agregar_contenedor_bottom(self, contenedor):
        """ Agrega widget de la salida del compilador. """
        self.contenedor_bottom = contenedor
        self.contenedor_bottom.hide()
        self.split_principal.insertWidget(2, contenedor)

    def mostrar_ocultar_widget_bottom(self):
        """ Muestra/oculta widget secundario. """

        if self.contenedor_bottom.isVisible():
            self.contenedor_bottom.hide()
            w = self.contenedor_principal.devolver_widget_actual()
            if w:
                w.setFocus()
        else:
            self.contenedor_bottom.show()

    def visibilidad_contenedor_principal(self):
        if self.contenedor_principal.isVisible():
            self.contenedor_principal.hide()
        else:
            self.contenedor_principal.show()

    def visibilidad_lateral(self):
        if self.lateral.isVisible():
            self.lateral.hide()
        else:
            self.lateral.show()

    def showEvent(self, evento):
        QWidget.showEvent(self, evento)
        self.split_horizontal.insertWidget(1, self.split_principal)
        alto = [self.height() / 3 * 2, self.height() / 3]
        ancho = [self.width() / 6 * 5, self.width() / 6]
        size_principal = [alto[1], alto[0]]
        size_horizontal = [ancho[1], ancho[0]]
        self.split_principal.setSizes(size_principal)
        self.split_horizontal.setSizes(size_horizontal)


class Lateral(QWidget):

    def __init__(self, lateral):
        super(Lateral, self).__init__()
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(5, 0, 0, 0)
        layoutV.addWidget(lateral)

        self.label_info = QLabel(self.trUtf8(""))
        layoutV.addWidget(self.label_info)

    def set_info_simbolo(self, info):
        self.label_info.setText(info)