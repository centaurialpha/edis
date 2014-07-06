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

from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from edis_c.interfaz import widget_buscar
from edis_c import recursos


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, ide):
        super(MenuBuscar, self).__init__()

        self.ide = ide

        # Shortcut
        self.atajoBuscar = QShortcut(recursos.ATAJOS['buscar'], self.ide)

        # Conexión
        self.connect(self.atajoBuscar, SIGNAL("activated()"),
            widget_buscar.WidgetBuscar().show)

        accionBuscar = menu_buscar.addAction(self.trUtf8("Buscar"))

        self.connect(accionBuscar, SIGNAL("triggered()"),
            widget_buscar.WidgetBuscar().show)