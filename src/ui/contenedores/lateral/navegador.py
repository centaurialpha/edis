# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    )

from PyQt4.QtCore import (
    SIGNAL,
    pyqtSignal
    )


class Navegador(QListWidget):

    cambiar_editor = pyqtSignal(int)

    def __init__(self):
        super(Navegador, self).__init__()
        self.connect(self, SIGNAL("clicked(QModelIndex)"),
                    self._cambiar_editor)

    def agregar(self, archivo):
        self.addItem(archivo)

    def eliminar(self, indice):
        self.takeItem(indice)

    def cambiar_foco(self, indice):
        self.setCurrentRow(indice)

    def _cambiar_editor(self):
        indice = self.row(self.currentItem())
        self.cambiar_editor.emit(indice)