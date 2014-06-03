#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, ide):
        super(MenuBuscar, self).__init__()

        accionBuscar = menu_buscar.addAction(self.trUtf8("Buscar"))
        accionBuscar.setShortcut(Qt.CTRL + Qt.Key_F)