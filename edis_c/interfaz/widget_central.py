#-*- coding: utf-8 -*-

# <Agrega el contenedor lateral, central y el output.>
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

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QVBoxLayout

# Módulos QtCore
from PyQt4.QtCore import Qt


class WidgetCentral(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        layout_horizontal = QVBoxLayout(self)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)

        self.split_principal = QSplitter(Qt.Vertical)
        self.layout = QVBoxLayout()
        layout_horizontal.addWidget(self.split_principal)
        layout_horizontal.addLayout(self.layout)

    def agregar_contenedor_central(self, contenedor):
        self.contenedor_principal = contenedor
        self.split_principal.insertWidget(0, contenedor)

    def agregar_buscador(self, buscador):
        self.buscador = buscador
        self.buscador.hide()
        self.layout.addWidget(buscador)

    def agregar_buscador_de_archivos(self, buscador):
        self.buscador_archivos = buscador
        self.buscador_archivos.hide()
        self.layout.addWidget(buscador)

    def agregar_contenedor_bottom(self, contenedor):
        self.contenedor_bottom = contenedor
        self.contenedor_bottom.hide()
        self.split_principal.insertWidget(1, contenedor)

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