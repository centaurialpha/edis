# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    QListWidgetItem,
    QColor,
    QMenu
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.ui.main import Edis


class SalidaCompilador(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setStyleSheet(
            "QListWidget { background: #1a1d1f }")
        self._parent = parent
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Conexión
        self.connect(self, SIGNAL("itemClicked(QListWidgetItem*)"),
                     self._go_to_line)
        self.connect(self, SIGNAL("customContextMenuRequested(const QPoint)"),
                     self._load_context_menu)

    def stderr_output(self):
        process = self._parent.build_process
        texto = process.readAllStandardError().data().decode('utf-8')
        for linea in texto.splitlines():
            item = None
            if linea.find(': warning') != -1:
                item = Item(linea, self)
                item.setForeground(QColor("#D4D443"))
                item.clickeable = True
                self.addItem(item)
            elif linea.find(': error') != -1:
                item = Item(linea, self)
                item.setForeground(QColor("#df3e3e"))
                item.clickeable = True
                self.addItem(item)
            elif linea.find('^') != -1:
                item = Item(linea, self)
                item.setForeground(QColor("#00b34b"))
                self.addItem(item)
            else:
                normal = Item(linea, self)
                self.addItem(normal)
            if item is not None:
                if item.clickeable:
                    item.setToolTip(self.tr("Click para ir a la línea"))

    def _go_to_line(self, item):
        if item.clickeable:
            editor_container = Edis.get_component("principal")
            line = self._parse_line(item)
            editor_container.go_to_line(line)

    def _parse_line(self, item):
        data = item.text()
        for l in data.split(':'):
            if l.isdigit():
                line = int(l)
                break  # El segundo item es el número de columna
        return line - 1

    def _load_context_menu(self, point):
        menu = QMenu()
        clear_action = menu.addAction(self.tr("Limpiar"))
        self.connect(clear_action, SIGNAL("triggered()"), self.clear)
        menu.exec_(self.mapToGlobal(point))


class Item(QListWidgetItem):

    def __init__(self, text, parent=None, italic=False):
        QListWidgetItem.__init__(self, text, parent)
        font = self.font()
        font.setPointSize(10)
        if italic:
            font.setItalic(True)
        self.setFont(font)
        self.clickeable = False
