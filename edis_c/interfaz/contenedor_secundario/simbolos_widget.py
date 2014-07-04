#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QAbstractItemView


class SimbolosWidget(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)