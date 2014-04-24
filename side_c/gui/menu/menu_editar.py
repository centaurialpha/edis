#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject


class MenuEditar(QObject):

    def __init__(self, menu_editar, ide):
        super(MenuEditar, self).__init__()

        accionPreferencias = menu_editar.addAction(self.tr("Preferencias"))

        accionPreferencias.triggered.connect(self.show_preferencias)

    def show_preferencias(self):
        pass