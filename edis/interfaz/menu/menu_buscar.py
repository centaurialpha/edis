#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

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
    QToolButton,
    QIcon
    )

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from edis import recursos
from edis.interfaz.editor import acciones_
from edis.interfaz.widgets.creador_widget import crear_accion

_ATAJO = recursos.ATAJOS
_ICONO = recursos.ICONOS


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, toolbar, ide):
        super(MenuBuscar, self).__init__()

        self.ide = ide

        # Acciones #
        # Buscar
        accionBuscar = crear_accion(self, "Buscar", icono=_ICONO['buscar'])

        # Ir a la línea
        accionIrALinea = crear_accion(self, "Ir a la línea...",
        atajo=_ATAJO['ir'], slot=self.ir_a_la_linea)

        # Agregar acción al menú #
        menu_buscar.addAction(accionBuscar)
        menu_buscar.addSeparator()
        menu_buscar.addAction(accionIrALinea)

        self.tool_buscar = QToolButton()
        self.tool_buscar.setDefaultAction(accionBuscar)
        self.tool_buscar.setIcon(QIcon(_ICONO['buscar']))

        self.items_toolbar = {
            'buscar': self.tool_buscar
            }

    def ir_a_la_linea(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.ir_a_la_linea(editor)

    def buscar(self):
        if self.ide.buscador.isVisible():
            self.ide.buscador.hide()
        else:
            self.ide.buscador.show()
            self.ide.buscador.widget_buscar.line_edit.setFocus()