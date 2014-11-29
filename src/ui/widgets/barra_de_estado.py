# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    )

from src import recursos
from src.ui.widgets.creador_widget import create_button


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self)

        self.edis = parent

        self.nombre_archivo = NombreArchivo()
        self.estado_cursor = WidgetLineaColumna()
        self.archivo_modificado = MensajeArchivoModificado()

        self._widgets = [
            self.nombre_archivo,
            self.estado_cursor,
            self.archivo_modificado,
            ]

        # Load UI
        self.load_ui()

    def load_ui(self):
        """ Load the components of StatusBar """

        # Container
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        tool_lateral = create_button(self, icon=recursos.ICONOS['lateral'],
            text="Lateral", toggled=self._show_hide_lateral, text_beside=True)
        tool_lateral.setStyleSheet("color: gray")
        tool_output = create_button(self, icon=recursos.ICONOS['output'],
            text="Output", toggled=self._show_hide_output, text_beside=True)
        tool_output.setStyleSheet("color: gray")

        # Add the widgets to the container
        for w in self._widgets:
            widget = QWidget()
            widget.setSizePolicy(QSizePolicy.Expanding,
                                QSizePolicy.Expanding)
            box = QHBoxLayout(widget)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(w)
            layout.addWidget(widget)

        # Add the container to status bar
        self.addWidget(container, stretch=1)
        self.addWidget(tool_lateral)
        self.addWidget(tool_output)

    def mostrar_mensaje(self, mensaje, tiempo=3000):
        self.showMessage(mensaje, tiempo)

    def _show_hide_lateral(self):
        self.edis.widget_Central.show_hide_lateral()

    def _show_hide_output(self):
        self.edis.widget_Central.show_hide_output()


class NombreArchivo(QLabel):

    def __init__(self):
        super(NombreArchivo, self).__init__()
        self.setStyleSheet("color: gray")

    def cambiar_texto(self, archivo):
        self.setText(archivo)


class MensajeArchivoModificado(QLabel):

    def __init__(self):
        super(MensajeArchivoModificado, self).__init__()
        self.setStyleSheet("color: gray")
        self.setText('')

    def modificado(self, modificado=False):
        if modificado:
            self.setText(self.tr('Modificado'))
        else:
            self.setText('')


class WidgetLineaColumna(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setStyleSheet("color: gray")
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        hLayout = QHBoxLayout()
        self.texto = "Lin: %s/%s - Col: %s"
        self.posicion_cursor = QLabel(self.tr(self.texto % (0, 0, 0)))

        hLayout.addWidget(self.posicion_cursor)
        vLayout.addLayout(hLayout)

    def actualizar_posicion_cursor(self, linea, total, columna):
        self.posicion_cursor.setText(self.tr(
                                    self.texto % (linea, total, columna)))