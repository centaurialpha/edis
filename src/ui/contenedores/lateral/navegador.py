# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QListWidget

from PyQt4.QtCore import (
    SIGNAL,
    pyqtSignal
    )

from src.ui.edis_main import EDIS
from src.ui.contenedores.lateral import custom_dock


class Navegador(custom_dock.CustomDock):

    cambiar_editor = pyqtSignal(int)

    def __init__(self):
        custom_dock.CustomDock.__init__(self)
        self.navegador = QListWidget()
        self.navegador.connect(self, SIGNAL("clicked(QModelIndex)"),
                    self._cambiar_editor)
        self.setWidget(self.navegador)

        EDIS.cargar_lateral("navegador", self)

    def agregar(self, archivo):
        self.navegador.addItem(archivo)

    def eliminar(self, indice):
        self.navegador.takeItem(indice)

    def cambiar_foco(self, indice):
        self.navegador.setCurrentRow(indice)

    def _cambiar_editor(self):
        indice = self.navegador.row(self.navegador.currentItem())
        self.cambiar_editor.emit(indice)


navegador = Navegador()