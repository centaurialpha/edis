#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit


class Tab(QTabWidget):

    def __init__(self):
        QTabWidget.__init__(self)


class ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        self.salida_ = SalidaWidget(self)
        self.notas = Notas(self)

        self.tabs = Tab()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.addTab(self.salida_, "Salida")
        self.tabs.addTab(self.notas, "Notas")

        hlayout = QHBoxLayout()
        vlayout.addWidget(self.tabs)
        vlayout.addLayout(hlayout)


class SalidaWidget(QPlainTextEdit):
    """ Widget que muestra stdin/stderr. """

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)

        self.parent = parent
        # Solo lectura
        self.setReadOnly(True)


class Notas(QTextEdit):

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
