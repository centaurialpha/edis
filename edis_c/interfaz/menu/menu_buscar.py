#-*- coding: utf-8 -*-

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

from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from edis_c.interfaz.editor import acciones_
from edis_c import recursos


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, ide):
        super(MenuBuscar, self).__init__()

        self.ide = ide

        # Shortcut
        self.atajoBuscar = QShortcut(recursos.ATAJOS['buscar'], self.ide)

        # Conexión
        #self.connect(self.atajoBuscar, SIGNAL("activated()"),
            #widget_buscar.WidgetBuscar().show)

        # Acciones #
        # Buscar
        accionBuscar = menu_buscar.addAction(self.trUtf8("Buscar"))
        # Buscar siguiente
        accionBuscarSiguiente = menu_buscar.addAction(
            self.trUtf8("Buscar siguiente"))
        # Buscar anterior
        accionBuscarAnterior = menu_buscar.addAction(
            self.trUtf8("Buscar anterior"))
        # Reemplazar
        accionReemplazar = menu_buscar.addAction(
            self.trUtf8("Reemplazar"))
        menu_buscar.addSeparator()
        # Ir a la línea
        accionIrALinea = menu_buscar.addAction(
            self.trUtf8("Ir a la línea..."))

        accionIrALinea.triggered.connect(self.ir_a_la_linea)

    def ir_a_la_linea(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.ir_a_la_linea(editor)