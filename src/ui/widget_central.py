# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QHBoxLayout

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL


from src.ui.edis_main import EDIS


class WidgetCentral(QWidget):
    """ Clase contenedora de los widgets. """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.lateral = None
        layout_horizontal = QHBoxLayout(self)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)

        self.split_horizontal = QSplitter(Qt.Horizontal)
        self.split_horizontal.setObjectName('splith')
        self.split_principal = QSplitter(Qt.Vertical)
        self.layout = QHBoxLayout()

        layout_horizontal.addWidget(self.split_horizontal)
        layout_horizontal.addLayout(self.layout)

        EDIS.cargar_componente("central", self)

    def agregar_contenedor_central(self, contenedor):
        """ Agrega widget principal. """

        self.contenedor_principal = contenedor
        self.split_principal.insertWidget(0, contenedor)

    def agregar_contenedor_lateral(self, explorador):
        self.lateral = explorador
        self.split_horizontal.insertWidget(0, self.lateral)
        self.emit(SIGNAL("lateral()"))

    def agregar_contenedor_bottom(self, contenedor):
        """ Agrega widget de la salida del compilador. """
        self.contenedor_bottom = contenedor
        self.contenedor_bottom.hide()
        self.split_principal.insertWidget(2, contenedor)

    def show_hide_output(self):
        """ Muestra/oculta widget secundario. """

        if self.contenedor_bottom.isVisible():
            self.contenedor_bottom.hide()
            w = self.contenedor_principal.devolver_widget_actual()
            if w:
                w.setFocus()
        else:
            self.contenedor_bottom.show()

    def visibilidad_contenedor_principal(self):
        if self.contenedor_principal.isVisible():
            self.contenedor_principal.hide()
        else:
            self.contenedor_principal.show()

    def show_hide_lateral(self):
        if self.lateral.isVisible():
            self.lateral.hide()
        else:
            self.lateral.show()

    def showEvent(self, evento):
        QWidget.showEvent(self, evento)
        self.split_horizontal.insertWidget(1, self.split_principal)
        alto = [self.height() / 3 * 2, self.height() / 3]
        ancho = [self.width() / 6 * 5, self.width() / 6]
        size_principal = [alto[1], alto[0]]
        size_horizontal = [ancho[1], ancho[0]]
        self.split_principal.setSizes(size_principal)
        self.split_horizontal.setSizes(size_horizontal)

central = WidgetCentral()