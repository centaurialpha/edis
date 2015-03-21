# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    QListWidgetItem,
    QColor
    )

from PyQt4.QtCore import SIGNAL

from src.ui.main import Edis


class SalidaCompilador(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setStyleSheet("background: #000000; color: #FFFFFF")
        self._parent = parent

        # Conexión
        self.connect(self, SIGNAL("itemClicked(QListWidgetItem*)"),
                     self._go_to_line)

    def stderr_output(self):
        process = self._parent.build_process
        texto = process.readAllStandardError().data().decode('utf-8')
        for linea in texto.splitlines():
            item = None
            if linea.find(': warning') != -1:
                item = Item(linea, self)
                item.setForeground(QColor("#d4d443"))
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
                    item.setToolTip(self.tr("Click to go to the line"))

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


class Item(QListWidgetItem):

    def __init__(self, texto, parent=None):
        QListWidgetItem.__init__(self, texto, parent)
        fuente = self.font()
        fuente.setPointSize(10)
        self.setFont(fuente)
        self.clickeable = False
