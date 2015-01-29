# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    QListWidgetItem
    )

from PyQt4.QtCore import pyqtSignal


class SalidaCompilador(QListWidget):

    ir_a_linea = pyqtSignal(int)

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self._parent = parent
        self.itemClicked.connect(self._ir_a_linea)

    def parsear_salida_stderr(self):
        proceso = self._parent.proceso_compilacion
        texto = proceso.readAllStandardError().data().decode('utf-8')
        for linea in texto.splitlines():
            if linea.find(': warning') != -1:
                #FIXME: formato
                warning = Item(linea, self)
                warning.clickeable = True
                self.addItem(warning)
            elif linea.find(': error') != -1:
                #FIXME: formato
                error = Item(linea, self)
                error.clickeable = True
                self.addItem(error)
            else:
                normal = Item(linea, self)
                self.addItem(normal)

    def _ir_a_linea(self, item):
        if item.clickeable:
            linea = int(item.text().split(':')[1])
            self.ir_a_linea.emit(linea)


class Item(QListWidgetItem):

    def __init__(self, texto, parent=None):
        QListWidgetItem.__init__(self, texto, parent)
        self.clickeable = False
