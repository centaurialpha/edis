# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QListWidget

from src.ui.main import Edis
from src.ui.containers.lateral import custom_dock


class Navegador(custom_dock.CustomDock):

    def __init__(self):
        custom_dock.CustomDock.__init__(self)
        self.navegador = QListWidget()
        self.setWidget(self.navegador)

        self.navegador.itemClicked.connect(self._cambiar_editor)

        Edis.load_lateral("navigator", self)

    def add_item(self, archivo):
        self.navegador.addItem(archivo)

    def delete_item(self, indice):
        self.navegador.takeItem(indice)

    def cambiar_foco(self, indice):
        self.navegador.setCurrentRow(indice)

    def _cambiar_editor(self):
        indice = self.navegador.row(self.navegador.currentItem())
        principal = Edis.get_component("principal")
        principal.change_widget(indice)


navegador = Navegador()