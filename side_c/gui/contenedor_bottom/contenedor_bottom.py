#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPlainTextEdit


class ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        self.salida_ = SalidaWidget(self)
        hlayout = QHBoxLayout()
        vlayout.addWidget(self.salida_)
        vlayout.addLayout(hlayout)


class SalidaWidget(QPlainTextEdit):
    """ Widget que muestra stdin/stderr. """

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)

        self.parent = parent
        # Solo lectura
        self.setReadOnly(True)