#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QHBoxLayout

from PyQt4.QtCore import Qt


class WidgetCentral(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        layout_horizontal = QHBoxLayout(self)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)

        self.split_principal = QSplitter(Qt.Vertical)

        layout_horizontal.addWidget(self.split_principal)

    def agregar_contenedor_central(self, contenedor):
        self.contenedor_principal = contenedor
        self.split_principal.insertWidget(0, contenedor)

    def agregar_contenedor_bottom(self, contenedor):
        self.contenedor_bottom = contenedor
        self.contenedor_bottom.hide()
        self.split_principal.insertWidget(1, contenedor)

    def mostrar_ocultar_widget_bottom(self):
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