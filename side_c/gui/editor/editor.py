#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit
from PyQt4 import QtGui

import sys


class Editor(QPlainTextEdit):

    def __init__(self):
        super(Editor, self).__init__()


app = QtGui.QApplication(sys.argv)

w = Editor()
w.show()
sys.exit(app.exec_())