#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout

from PyQt4.QtCore import Qt


class WidgetCentral(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.split_lateral = None

        layout_horizontal = QHBoxLayout(self)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)

        self.split_principal = QSplitter(Qt.Vertical)
        self.split_lateral = QSplitter(Qt.Horizontal)

        layout_horizontal.addWidget(self.split_principal)
        layout_horizontal.addWidget(self.split_lateral)

    def agregar_contenedor_central(self, contenedor):
        self.contenedor_principal = contenedor
        #self.contenedor_principal.show()
        self.split_principal.insertWidget(0, contenedor)

    def agregar_contenedor_lateral(self, contenedor):
        self.contenedor_lateral = Lateral(contenedor)
        self.split_lateral.hide()
        self.split_lateral.insertWidget(1, contenedor)

    def agregar_contenedor_bottom(self, contenedor):
        self.contenedor_bottom = contenedor
        self.contenedor_bottom.hide()
        self.split_principal.insertWidget(1, contenedor)

    def showEvent(self, event):
        QWidget.showEvent(self, event)
        self.split_lateral.insertWidget(1, self.split_principal)
        self.split_lateral.setSizes([50, 200])

    def mostrar_ocultar_widget_bottom(self):
        """ Muestra/oculta widget secundario. """

        if self.contenedor_bottom.isVisible():
            self.contenedor_bottom.hide()
            w = self.contenedor_principal.actual_widget()
            if w:
                w.setFocus()
        else:
            self.contenedor_bottom.show()

    def mostrar_ocultar_widget_simbolos(self):
        if self.split_lateral.isVisible():
            self.split_lateral.hide()
        else:
            self.split_lateral.show()


class Lateral(QWidget):

    def __init__(self, widget_simbolos):
        QWidget.__init__(self)

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        layoutV.addWidget(widget_simbolos)