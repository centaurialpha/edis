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

# Módulos QtGui
from PyQt4.QtGui import QWidget
#from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QHeaderView

# Módulos QtCore
from PyQt4.QtCore import Qt

# Módulos EDIS
from src import recursos
#from edis.interfaz.c
from src.ui.contenedor_secundario import (
    procesos,
    logging_widget
    )


class ContenedorSecundario(QWidget):

    instancia = None

    def __new__(clase, *args, **kargs):
        if clase.instancia is None:
            clase.instancia = QWidget.__new__(clase, *args, **kargs)
        return clase.instancia

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layoutV = QVBoxLayout()

        layoutH = QHBoxLayout(self)
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)

        self.stack = Stacked()
        layoutH.addWidget(self.stack)

        self._toolbar = QToolBar()
        self._toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._toolbar.setObjectName('custom')
        self._toolbar.setOrientation(2)

        self.salida_ = procesos.EjecutarWidget()
        self.stack.addWidget(self.salida_)

        self.notas = Notas(self)
        self.stack.addWidget(self.notas)

        self.logging = logging_widget.Logging(self)
        #self.stack.addWidget(self.logging)

        self.boton_logging = QToolButton()
        self.boton_logging.setText(self.tr("Log"))

        self.botonSalida = QToolButton()
        self.botonSalida.setIcon(QIcon(recursos.ICONOS['terminal']))
        self.botonNotas = QToolButton()
        self.botonNotas.setIcon(QIcon(recursos.ICONOS['notas']))
        boton_cerrar = QToolButton()
        boton_cerrar.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton)))

        layoutV.addWidget(self._toolbar)
        #self._toolbar.addWidget(self.boton_logging)
        self._toolbar.addWidget(self.botonSalida)
        self._toolbar.addWidget(self.botonNotas)
        self._toolbar.addWidget(boton_cerrar)
        layoutH.addLayout(layoutV)

        # Conexiones
        self.atajoEscape = QShortcut(QKeySequence(Qt.Key_Escape),
            self)
        self.botonSalida.clicked.connect(lambda: self.item_cambiado(0))
        self.botonNotas.clicked.connect(lambda: self.item_cambiado(1))
        self.boton_logging.clicked.connect(lambda: self.item_cambiado(2))
        boton_cerrar.clicked.connect(self.hide)
        self.atajoEscape.activated.connect(self.hide)

    def item_cambiado(self, v):
        if not self.isVisible():
            self.show()

        self.stack.show_display(v)

    def compilar(self, path):
        self.item_cambiado(0)
        self.show()
        self.nombre_archivo = path
        self.salida_.correr_compilacion(self.nombre_archivo)
        self.salida_.output.setFoco()

    def ejecutar(self):
        #FIXME: revisar!
        if self.salida_.compilado:
            self.salida_.correr_programa()

    def frenar(self):
        self.salida_.terminar_proceso()

    def showEvent(self, evento):
        super(ContenedorSecundario, self).showEvent(evento)
        w = self.stack.currentWidget()
        if w:
            w.setFocus()


class Notas(QTextEdit):

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setText(self.trUtf8("Acá puedes escribir notas..."))


class SalidaCompilador(QWidget):

    def __init__(self, parent):
        super(SalidaCompilador, self).__init__(parent)
        vbox = QVBoxLayout(self)
        self.tabla = QTableWidget(0, 3)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setHorizontalHeaderLabels((self.trUtf8("Archivo"),
            self.trUtf8("Línea"), self.trUtf8("Error")))
        self.tabla.horizontalHeader().setResizeMode(
            2, QHeaderView.Stretch)
        self.tabla.setShowGrid(True)
        vbox.addWidget(self.tabla)

        item = QTableWidgetItem('Hola')
        fila = self.tabla.rowCount()
        self.tabla.insertRow(fila)
        self.tabla.setItem(fila, 0, item)


class Stacked(QStackedWidget):

    def __init__(self):
        QStackedWidget.__init__(self)

    def setCurrentIndex(self, index):
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)