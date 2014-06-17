#-*- coding: utf-8 -*-

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout

from PyQt4.QtCore import SIGNAL


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)

        self.widget = QWidget()
        v_layout = QVBoxLayout(self.widget)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.widget)

        self.connect(self, SIGNAL("messageChanged(QString)"),
            self.mensaje_terminado)

    def showMessage(self, mensaje, tiempo):
        self.widget.hide()
        QStatusBar.showMessage(self, mensaje, tiempo)

    def mensaje_terminado(self, mensaje):
        if not mensaje:
            self.hide()