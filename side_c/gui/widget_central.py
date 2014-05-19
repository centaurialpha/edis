#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QVBoxLayout

from PyQt4.QtCore import Qt
from side_c.gui import tab_widget
from side_c.gui import editor


class WidgetCentral(QWidget):

    def __init__(self):
        super(WidgetCentral, self).__init__()

        layout_vertical = QVBoxLayout(self)

        self.tabs = tab_widget.TabCentral()
        self.split_horizontal = QSplitter(Qt.Horizontal)
        self.split_horizontal.addWidget(self.tabs)
        layout_vertical.addWidget(self.split_horizontal)