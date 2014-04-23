#-*- coding: utf-8 -*-
"""

menu acerca de

"""
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject

from side_c.gui.dialogos import dialogo_acerca_de_ide


class MenuAcercade(QObject):

    def __init__(self, menu_acerca_de, ide):
        super(MenuAcercade, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide
        acerca_ide = menu_acerca_de.addAction(self.tr("Acerca de IDE"))
        acerca_qt = menu_acerca_de.addAction(self.tr("Acerca de Qt"))

        # Conexiones
        acerca_ide.triggered.connect(self.acerca_de_ide)
        acerca_qt.triggered.connect(self.acerca_de_qt)

    def acerca_de_ide(self):
        self.acerca_de = dialogo_acerca_de_ide.AcercaDeIDE()
        self.acerca_de.show()

    def acerca_de_qt(self):
        QMessageBox.aboutQt(self.ide, 'Acerca de Qt')