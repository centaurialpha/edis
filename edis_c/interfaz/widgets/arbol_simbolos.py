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

from subprocess import Popen

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QHeaderView
    )

from PyQt4.QtCore import QThread


class ArbolDeSimbolos(QTreeWidget):

    def __init__(self):
        super(ArbolDeSimbolos, self).__init__()
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.header().setStretchLastSection(False)
        self.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)

    def actualizar_simbolos(self, simbolos):
        self.clear()
        funciones = QTreeWidgetItem(self)
        structs = QTreeWidgetItem(self)

        if 'funciones' in simbolos:
            funciones.setText(0, self.tr("Funciones"))
            for f in simbolos['funciones']:
                funcion = QTreeWidgetItem(funciones)
                funcion.setText(0, f)
        if 'structs' in simbolos:
            structs.setText(0, self.tr("Structs"))
            for s in simbolos['structs']:
                struct = QTreeWidgetItem(structs)
                struct.setText(0, s)

        funciones.setExpanded(True)
        structs.setExpanded(True)


class ThreadSimbolos(QThread):

    def __init__(self):
        super(ThreadSimbolos, self).__init__()
        self.archivo = ''

    def run(self):
        simbolos = {}
        funciones = []
        structs = []

        ctags = "ctags %s"
        Popen(ctags % self.archivo, shell=True)
        with open('tags') as tag:
            archivo = tag.read()

        for f in archivo.rstrip().split('\n'):
            if f.startswith('!'):
                continue
            if f.endswith('f'):
                funciones.append(f.split()[0])
            if f.endswith('file:') and f.split()[-2] == 's':
                structs.append(f.split()[0])
        if len(funciones) > 0:
            simbolos['funciones'] = funciones
        if len(structs) > 0:
            simbolos['structs'] = structs

        return simbolos