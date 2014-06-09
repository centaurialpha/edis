#-*- coding: utf-8 -*-

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)

        self.widget = QWidget()
        v_layout = QVBoxLayout(self.widget)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.widget)