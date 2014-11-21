# -*- coding: utf-8 -*-

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
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy
    )


from src import recursos
from src.ui.widgets.creador_widget import create_button


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        super(BarraDeEstado, self).__init__()
        self.edis = parent

        self.nombre_archivo = NombreArchivo()
        self.estado_cursor = WidgetLineaColumna()
        self.archivo_modificado = MensajeArchivoModificado()

        widget_filename = QWidget()
        widget_filename.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        box_filename = QHBoxLayout(widget_filename)
        box_filename.addWidget(self.nombre_archivo)

        widget_modified = QWidget()
        widget_modified.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Ignored)
        box_modified = QHBoxLayout(widget_modified)
        box_modified.addWidget(self.archivo_modificado)

        widget_cursor = QWidget()
        widget_cursor.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        box_cursor = QHBoxLayout(widget_cursor)
        box_cursor.addWidget(self.estado_cursor)

        widget_tools = QWidget()
        self.tool_view_lateral = create_button(self,
            icon=recursos.ICONOS['lateral'], toggled=self._show_hide_lateral)
        self.tool_view_lateral.setCheckable(True)

        self.tool_view_lateral.setAutoRaise(True)
        self.tool_view_output = create_button(self,
            icon=recursos.ICONOS['output'], toggled=self._show_hide_output)
        self.tool_view_output.setCheckable(True)
        self.tool_view_output.setAutoRaise(True)

        box_tools = QHBoxLayout(widget_tools)
        box_tools.addWidget(self.tool_view_lateral)
        box_tools.addWidget(self.tool_view_output)

        self.addWidget(widget_filename, stretch=1)
        self.addWidget(widget_cursor, stretch=1)
        self.addWidget(widget_modified, stretch=1)
        self.addWidget(widget_tools)

    def mostrar_mensaje(self, mensaje, tiempo=3000):
        self.showMessage(mensaje, tiempo)

    def _show_hide_lateral(self):
        self.edis.widget_Central.show_hide_lateral()

    def _show_hide_output(self):
        self.edis.widget_Central.show_hide_output()


class NombreArchivo(QLabel):

    def __init__(self):
        super(NombreArchivo, self).__init__()

    def cambiar_texto(self, archivo):
        self.setText(archivo)


class MensajeArchivoModificado(QLabel):

    def __init__(self):
        super(MensajeArchivoModificado, self).__init__()
        self.setText('')

    def modificado(self, modificado=False):
        if modificado:
            self.setText(self.tr('Modificado'))
        else:
            self.setText('')


class WidgetLineaColumna(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        hLayout = QHBoxLayout()
        self.texto = "Lin: %s/%s - Col: %s"
        self.posicion_cursor = QLabel(self.trUtf8(self.texto % (0, 0, 0)))

        hLayout.addWidget(self.posicion_cursor)
        vLayout.addLayout(hLayout)

    def actualizar_posicion_cursor(self, linea, total, columna):
        self.posicion_cursor.setText(self.tr(
                                    self.texto % (linea, total, columna)))