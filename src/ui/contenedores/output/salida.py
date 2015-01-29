# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    QListWidgetItem,
    QColor
    )

from PyQt4.QtCore import pyqtSignal


class SalidaCompilador(QListWidget):

    ir_a_linea = pyqtSignal(int)

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setObjectName("salida_compilador")
        self._parent = parent
        self.itemClicked.connect(self._ir_a_linea)

    def parsear_salida_stderr(self):
        proceso = self._parent.proceso_compilacion
        texto = proceso.readAllStandardError().data().decode('utf-8')
        for linea in texto.splitlines():
            if linea.find(': warning') != -1:
                warning = Item(linea, self)
                warning.setForeground(QColor("#d4d443"))
                self.addItem(warning)
            elif linea.find(': error') != -1:
                error = Item(linea, self)
                error.setForeground(QColor("#e73e3e"))
                self.addItem(error)
            elif linea.find('^') != -1:
                shap = Item(linea, self)
                shap.setForeground(QColor("#00b34b"))
                self.addItem(shap)
            else:
                normal = Item(linea, self)
                normal.clickeable = False
                self.addItem(normal)

    def _ir_a_linea(self, item):
        if item.clickeable:
            linea = int(item.text().split(':')[1]) - 1
            self.ir_a_linea.emit(linea)


class Item(QListWidgetItem):

    def __init__(self, texto, parent=None):
        QListWidgetItem.__init__(self, texto, parent)
        fuente = self.font()
        fuente.setPointSize(10)
        self.setFont(fuente)
        self.clickeable = True