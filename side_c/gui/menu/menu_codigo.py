#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QObject

from side_c import recursos


class MenuCodigoFuente(QObject):

    def __init__(self, menu_codigo, ide):
        super(MenuCodigoFuente, self).__init__()

        accionCompilar = menu_codigo.addAction(
            self.trUtf8("Compilar"))
        accionEjecutar = menu_codigo.addAction(
            self.trUtf8("Ejecutar"))
        accionCompilar_Ejecutar = menu_codigo.addAction(
            self.trUtf8("Compilar y ejecutar"))