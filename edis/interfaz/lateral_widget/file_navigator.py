# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import (
    QWidget,
    QAction,
    QMenu,
    QStandardItemModel,
    QStandardItem,
    QVBoxLayout,
    QIcon,
    QAbstractItemView,
    QListView
    )
from PyQt4.QtCore import (
    SIGNAL,
    QModelIndex,
    pyqtSlot,
    Qt
    )

from edis import recursos
from edis.interfaz.contenedor_principal import contenedor_principal


class Navegador(QWidget):

    def __init__(self, parent=None):
        super(Navegador, self).__init__(parent)
        self.parent = parent
        self.archivos = []

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.lista = ListView(self)
        self.lista.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.model = QStandardItemModel(self.lista)
        vbox.addWidget(self.lista)
        self.lista.clicked.connect(self.cambiar_tab)

    @pyqtSlot(QModelIndex)
    def cambiar_tab(self, indice):

        self.emit(SIGNAL("cambioPes(int)"), indice.row())

    def cargar_archivos(self, archivos):
        archivos = list(archivos)

        for i in archivos:
            item = QStandardItem(i.split('/')[-1])
            if str(i[-1]).startswith('h'):
                item.setIcon(QIcon(recursos.ICONOS['cabecera']))
            if str(i[-1]).startswith('c'):
                item.setIcon(QIcon(recursos.ICONOS['c']))

            self.model.appendRow(item)
        self.lista.setModel(self.model)

    def borrar_item(self, item):

        self.model.removeRow(item)

    def get_archivos(self):
        return contenedor_principal.ContenedorMain().get_archivos()


class ListView(QListView):

    def __init__(self, parent):
        super(ListView, self).__init__()
        self.parent = parent

    def contextMenuEvent(self, evento):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        menu = QMenu(self)
        accionC = QAction('Cerrar', self)
        menu.addAction(accionC)
        accionC.triggered.connect(self.parent.borrar_item)
        menu.exec_(evento.globalPos())
