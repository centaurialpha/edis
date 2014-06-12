#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit
#from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget


class EjecutarWidget(QWidget):

    def __init__(self):
        super(EjecutarWidget, self).__init__()



class SalidaWidget(QPlainTextEdit):

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self._parent = parent
        self.setReadOnly(True)

