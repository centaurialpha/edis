# -*- coding: utf-8 -*-

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

from PyQt4.QtGui import (
    QTabWidget,
    )

from edis.nucleo import configuraciones
from edis.interfaz.widgets import arbol_simbolos


class LateralContainer(QTabWidget):

    def __init__(self, parent):
        super(LateralContainer, self).__init__()

        self.symbols_widget = None

        if configuraciones.SYMBOLS:
            self.add_symbols_widget()

    def add_symbols_widget(self):
        if not self.symbols_widget:
            self.symbols_widget = arbol_simbolos.ArbolDeSimbolos()
            self.addTab(self.symbols_widget, self.trUtf8("Símbolos"))