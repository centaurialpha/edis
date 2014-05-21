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
        self.contenedor_principal.show()
        self.split_principal.insertWidget(0, contenedor)