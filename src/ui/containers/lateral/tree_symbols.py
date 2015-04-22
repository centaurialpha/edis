# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
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


class ArbolDeSimbolos(QTreeWidget):

    goToLine = pyqtSignal(int)

    def __init__(self):
        QTreeWidget.__init__(self)
        self.setObjectName("simbolos")
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.header().setStretchLastSection(False)
        self.header().setHorizontalScrollMode(
            QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)

        # Conexión
        self.itemClicked[QTreeWidgetItem, int].connect(self.go_to_line)
        self.itemActivated[QTreeWidgetItem, int].connect(self.go_to_line)

        Edis.load_lateral("symbols", self)

    def update_symbols(self, symbols):
        # Limpiar
        self.clear()

        if 'globals' in symbols:
            _globals = Item(self, [self.tr("Variables")])
            _globals.clicked = False
            for _glob, nline in sorted(list(symbols['globals'].items())):
                _global = Item(_globals, [_glob])
                _global.line = nline
                _global.setIcon(0, QIcon(":image/variable"))
            _globals.setExpanded(True)

        if 'functions' in symbols:
            functions = Item(self, [self.tr('Functions')])
            functions.clicked = False
            for nline, func in sorted(list(symbols['functions'].items())):
                function = Item(functions, [func])
                function.line = nline
                function.setIcon(0, QIcon(":image/function"))
            functions.setExpanded(True)

        if 'structs' in symbols:
            structs = Item(self, [self.tr("Structs")])
            structs.clicked = False
            for nline, name in sorted(list(symbols['structs'].items())):
                struct = Item(structs, [name])
                struct.line = nline
                struct.setIcon(0, QIcon(":image/struct"))
            structs.setExpanded(True)

        if 'members' in symbols:
            members = Item(self, [self.tr("Members")])
            members.clicked = False
            for name, data in sorted(list(symbols['members'].items())):
                info = "%s [%s]" % (name, data[1])
                member = Item(members, [info])
                member.line = data[0]
                member.setIcon(0, QIcon(":image/member"))
            members.setExpanded(True)

        if 'enums' in symbols:
            enums = Item(self, [self.tr("Enums")])
            enums.clicked = False
            for nline, name in sorted(list(symbols['enums'].items())):
                enum = Item(enums, [name])
                enum.line = nline
                enum.setIcon(0, QIcon(":image/enum"))
            enums.setExpanded(True)

    def go_to_line(self, item):
        if item.clicked:
            self.goToLine.emit(int(item.line) - 1)


# Custom item basado en QTreeWidgetItem
Item = type('Item', (QTreeWidgetItem,), {'line': None, 'clicked': True})


simbolos = ArbolDeSimbolos()
