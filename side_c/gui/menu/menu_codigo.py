#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt

from side_c import recursos


class MenuCodigoFuente(QObject):

    def __init__(self, menu_codigo, toolbar, ide):
        super(MenuCodigoFuente, self).__init__()

        accionCompilar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['compilar']), self.trUtf8("Compilar"))
        accionCompilar.setShortcut(Qt.CTRL + Qt.Key_F5)
        accionEjecutar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['ejecutar']), self.trUtf8("Ejecutar"))
        accionEjecutar.setShortcut(Qt.CTRL + Qt.Key_F6)
        accionCompilar_Ejecutar = menu_codigo.addAction(
            self.trUtf8("Compilar y ejecutar"))

        self.items_toolbar = {
            "compilar-archivo": accionCompilar,
            "ejecutar-archivo": accionEjecutar,
            "ejecutar_compilar-archivo": accionCompilar_Ejecutar
            }