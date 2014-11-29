# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QToolButton,
    QIcon
    )

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from src import recursos
from src.ui.editor import acciones_
from src.ui.widgets.creador_widget import crear_accion

_ATAJO = recursos.ATAJOS
_ICONO = recursos.ICONOS


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, toolbar, ide):
        super(MenuBuscar, self).__init__()

        self.ide = ide

        # Acciones #
        # Buscar
        accionBuscar = crear_accion(self, "Buscar", icono=_ICONO['buscar'],
            atajo=_ATAJO['buscar'], slot=self.buscar)

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
        self.ide.contenedor_principal.tab.mostrar_popup()