#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4 import QtGui
import sys


class AcercaDeIDE(QDialog):

    def __init__(self):
        super(AcercaDeIDE, self).__init__()


app = QtGui.QApplication(sys.argv)
w = AcercaDeIDE()
w.show()
sys.exit(app.exec_())