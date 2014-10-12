# -*- coding: utf-8 -*-

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

from PyQt4.QtGui import (
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
    )


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        super(BarraDeEstado, self).__init__()

        separador = Separador()
        separador2 = Separador()
        separador3 = Separador()

        self.contenedor = QWidget()

        hLayout = QHBoxLayout(self.contenedor)
        hLayout.setContentsMargins(0, 0, 0, 0)

        self.nombre_archivo = NombreArchivo()
        self.estado_cursor = WidgetLineaColumna(self)
        self.archivo_guardado = MensajeArchivoGuardado(self)

        hLayout.addWidget(self.nombre_archivo)
        hLayout.addWidget(separador)
        hLayout.addWidget(self.estado_cursor)
        hLayout.addWidget(separador2)
        hLayout.addWidget(self.archivo_guardado)
        hLayout.addWidget(separador3)

        self.addWidget(self.contenedor)

    def mostrar_mensaje(self, mensaje, tiempo=3000):
        self.showMessage(mensaje, tiempo)


class NombreArchivo(QLabel):

    def __init__(self):
        super(NombreArchivo, self).__init__()

    def cambiar_texto(self, archivo):
        self.setText(archivo)


class MensajeArchivoGuardado(QLabel):

    def __init__(self, parent):
        super(MensajeArchivoGuardado, self).__init__()
        self.setText('')

    def modificado(self, modificado=False):
        if modificado:
            self.setText(self.tr('Modificado'))
        else:
            self.setText('')


class Separador(QFrame):

    def __init__(self):
        super(Separador, self).__init__()
        self.setFrameStyle(QFrame.VLine | QFrame.Sunken)


class WidgetLineaColumna(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

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