#-*- coding: utf-8 -*-
"""

menu acerca de

"""

from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject

"""
import sys
sys.path.append("../")
import ide
"""


class MenuAcercade(QObject):

    def __init__(self, menu_acerca_de, ide):
        super(MenuAcercade, self).__init__()

        acerca_ide = menu_acerca_de.addAction(self.tr("Acerca de IDE"))
        acerca_qt = menu_acerca_de.addAction(self.tr("Acerca de Qt"))

        # Conexiones
        acerca_ide.triggered.connect(self.acerca_de_ide)
        acerca_qt.triggered.connect(self.acerca_de_qt)

    def acerca_de_ide(self):
        pass

    def acerca_de_qt(self):
        QMessageBox.aboutQt(ide.IDE(), 'Acerca de Qt')