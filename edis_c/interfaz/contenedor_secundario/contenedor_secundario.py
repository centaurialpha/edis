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

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QStyle
#from PyQt4.QtGui import QSizePolicy

from PyQt4.QtCore import SIGNAL

from edis_c.interfaz.contenedor_secundario import salida_widget
from edis_c import recursos


_instanciaContenedorSecundario = None


def ContenedorBottom(*args, **kw):
    global _instanciaContenedorSecundario
    if _instanciaContenedorSecundario is None:
        _instanciaContenedorSecundario = _ContenedorBottom(*args, **kw)

    return _instanciaContenedorSecundario


class _ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layoutV = QVBoxLayout()

        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        self.stack = Stacked()
        hbox.addWidget(self.stack)

        self.salida_ = salida_widget.EjecutarWidget()
        self.stack.addWidget(self.salida_)

        self.notas = Notas(self)
        self.stack.addWidget(self.notas)

        self.botonSalida = QPushButton(QIcon(recursos.ICONOS['terminal']), '')
        self.botonNotas = QPushButton(QIcon(recursos.ICONOS['notas']), '')
        boton_cerrar = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogCloseButton), '')

        layoutV.addWidget(self.botonSalida)
        layoutV.addWidget(self.botonNotas)
        #layoutV.addSpacerItem(QSpacerItem(0, 0, 0))
        layoutV.addWidget(boton_cerrar)
        hbox.addLayout(layoutV)

        self.connect(self.botonSalida, SIGNAL("clicked()"),
            lambda: self.item_cambiado(0))
        self.connect(self.botonNotas, SIGNAL("clicked()"),
            lambda: self.item_cambiado(1))
        self.connect(boton_cerrar, SIGNAL("clicked()"),
            self.hide)

    def item_cambiado(self, v):
        if not self.isVisible():
            self.show()

        self.stack.show_display(v)

    def compilar_archivo(self, salida, path):
        self.item_cambiado(0)
        self.show()
        self.s = salida
        self.path = path
        self.salida_.correr_compilacion(self.s, self.path)

    def ejecutar_archivo(self, comp):
        if comp:
            self.salida_.correr_programa()
        else:
            QMessageBox.information(self, self.trUtf8("Información"),
                self.trUtf8("No se ha compilado el fuente!"))


class Notas(QTextEdit):

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setText(self.trUtf8("Acá puedes escribir notas..."))


class Stacked(QStackedWidget):

    def __init__(self):
        QStackedWidget.__init__(self)

    def setCurrentIndex(self, index):
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)