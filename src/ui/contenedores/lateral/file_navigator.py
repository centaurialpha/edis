# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QAction,
    QMenu,
    QStandardItemModel,
    QStandardItem,
    QVBoxLayout,
    QAbstractItemView,
    QListView,
    )
from PyQt4.QtCore import (
    SIGNAL,
    QModelIndex,
    pyqtSlot,
    Qt
    )

from src.ui.contenedor_principal import contenedor_principal


class Navegador(QWidget):

    def __init__(self, parent=None):
        super(Navegador, self).__init__(parent)
        self.setObjectName("navegador")
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
        self.setStyleSheet(
            "QListView::item:selected{border: 1px solid white}")

    def contextMenuEvent(self, evento):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        menu = QMenu(self)
        accionC = QAction('Cerrar', self)
        menu.addAction(accionC)
        accionC.triggered.connect(self.parent.borrar_item)
        menu.exec_(evento.globalPos())

    def change_style(self, index):
        self.setStyleSheet(
            "QListView::item:selected{border: 1px solid white; color: #71afc9}")