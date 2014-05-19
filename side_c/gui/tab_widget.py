#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QTextEdit


class TabCentral(QTabWidget):

    def __init__(self):
        super(TabCentral, self).__init__()

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)