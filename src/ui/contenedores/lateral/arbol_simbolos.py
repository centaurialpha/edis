# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QIcon
    )

from PyQt4.QtCore import pyqtSignal

from src import paths
from src.ui.main import EDIS
from src.ui.contenedores.lateral import custom_dock


class ArbolDeSimbolos(custom_dock.CustomDock):

    _ir_a_linea = pyqtSignal(int, name='irALinea')

    iconos = {
        'clase': paths.ICONOS['class'],
        'funcion': paths.ICONOS['funcion'],
        'struct': paths.ICONOS['struct'],
        'miembro': paths.ICONOS['miembro'],
        'global': paths.ICONOS['variable'],
        'enumerator': paths.ICONOS['enumerator'],
        'enums': paths.ICONOS['enums']
        }

    def __init__(self):
        custom_dock.CustomDock.__init__(self)
        self.tree = QTreeWidget()
        self.setWidget(self.tree)
        self.tree.setObjectName("simbolos")
        self.tree.header().setHidden(True)
        self.tree.setSelectionMode(self.tree.SingleSelection)
        self.tree.setAnimated(True)
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setHorizontalScrollMode(
            QAbstractItemView.ScrollPerPixel)
        self.tree.header().setResizeMode(0, QHeaderView.ResizeToContents)

        # Conexión
        self.tree.itemClicked[QTreeWidgetItem, int].connect(self.ir_a_linea)
        self.tree.itemActivated[QTreeWidgetItem, int].connect(self.ir_a_linea)

        EDIS.cargar_lateral("simbolos", self)

    def actualizar_simbolos(self, simbolos):
        # Limpiar
        self.tree.clear()

        if 'globals' in simbolos:
            _globals = Item(self.tree, [self.tr("Globales")])
            _globals.clickeable = False
            for _glob, nline in list(simbolos['globals'].items()):
                _global = Item(_globals, [_glob])
                _global.linea = nline
                _global.setIcon(0, QIcon(self.iconos['global']))
            _globals.setExpanded(True)

        if 'functions' in simbolos:
            functions = Item(self.tree, [self.tr('Funciones')])
            functions.clickeable = False
            for line, func in list(simbolos['functions'].items()):
                function = Item(functions, [func])
                function.linea = line
                function.setIcon(0, QIcon(self.iconos['funcion']))
            functions.setExpanded(True)

    def ir_a_linea(self, item):
        if item.clickeable:
            self._ir_a_linea.emit(int(item.linea) - 1)


class Item(QTreeWidgetItem):

    def __init__(self, parent, nombre):
        QTreeWidgetItem.__init__(self, parent, nombre)
        self.linea = None
        self.clickeable = True


simbolos = ArbolDeSimbolos()