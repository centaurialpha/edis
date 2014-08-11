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
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QLabel


class ConfiguracionTema(QWidget):

    def __init__(self, parent):
        super(ConfiguracionTema, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        self.lista_temas = QListWidget()
        self.lista_temas.addItem("Por defecto")
        self.lista_temas.addItem("Black SIDE")

        label = QLabel(self.trUtf8("Elige un tema:"))

        layoutV.addWidget(label)
        layoutV.addWidget(self.lista_temas)
