# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QIcon
    )

from PyQt4.QtCore import pyqtSignal

from src.ui.main import Edis
from src.ui.containers.lateral import custom_dock


class ArbolDeSimbolos(custom_dock.CustomDock):

    goToLine = pyqtSignal(int)

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
        self.tree.itemClicked[QTreeWidgetItem, int].connect(self.go_to_line)
        self.tree.itemActivated[QTreeWidgetItem, int].connect(self.go_to_line)

        Edis.load_lateral("symbols", self)

    def update_symbols(self, symbols):
        # Limpiar
        self.tree.clear()

        if 'globals' in symbols:
            _globals = Item(self.tree, [self.tr("Globals")])
            _globals.clicked = False
            for _glob, nline in sorted(list(symbols['globals'].items())):
                _global = Item(_globals, [_glob])
                _global.line = nline
                _global.setIcon(0, QIcon(":image/variable"))
            _globals.setExpanded(True)

        if 'functions' in symbols:
            functions = Item(self.tree, [self.tr('Functions')])
            functions.clicked = False
            for nline, func in sorted(list(symbols['functions'].items())):
                function = Item(functions, [func])
                function.line = nline
                function.setIcon(0, QIcon(":image/function"))
            functions.setExpanded(True)

        if 'structs' in symbols:
            structs = Item(self.tree, [self.tr("Structs")])
            structs.clicked = False
            for nline, item in sorted(list(symbols['structs'].items())):
                struct = Item(structs, [item[0]])
                struct.line = nline
                struct.setIcon(0, QIcon(":image/struct"))
                members = item[1]
                for name, nline in sorted(list(members.items())):
                    member = Item(struct, [name])
                    member.line = nline
                    member.setIcon(0, QIcon(":image/member"))
                struct.setExpanded(True)
            structs.setExpanded(True)

    def go_to_line(self, item):
        if item.clicked:
            self.goToLine.emit(int(item.line) - 1)


# Custom item basado en QTreeWidgetItem
Item = type('Item', (QTreeWidgetItem,), {'line': None, 'clicked': True})


simbolos = ArbolDeSimbolos()