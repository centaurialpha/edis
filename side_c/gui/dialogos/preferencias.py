#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSize


class PreferenciasWidget(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle(self.tr("SIDE-C - Preferencias"))
        self.setMaximumSize(QSize(0, 0))
