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
            if linea.find(': warning') != -1:
                warning = Item(linea, self)
                warning.setForeground(QColor("#d4d443"))
                warning.clickeable = True
                self.addItem(warning)
            elif linea.find(': error') != -1:
                error = Item(linea, self)
                error.setForeground(QColor("#df3e3e"))
                error.clickeable = True
                self.addItem(error)
            elif linea.find('^') != -1:
                shap = Item(linea, self)
                shap.setForeground(QColor("#00b34b"))
                self.addItem(shap)
            else:
                normal = Item(linea, self)
                self.addItem(normal)

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
