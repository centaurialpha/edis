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

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QIcon
    )

from PyQt4.QtCore import (
    SIGNAL
    )

from edis_c import recursos


class ArbolDeSimbolos(QTreeWidget):
    iconos = {
        'funcion': recursos.ICONOS['funcion'],
        'struct': recursos.ICONOS['struct'],
        'miembro': recursos.ICONOS['miembro'],
        'global': recursos.ICONOS['variable'],
        'enumerator': recursos.ICONOS['enumerator'],
        'enums': recursos.ICONOS['enums']
        }

    def __init__(self):
        super(ArbolDeSimbolos, self).__init__()
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.header().setStretchLastSection(False)
        self.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)

        self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.info_item)
        self.connect(self, SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.info_item)
        self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.ir_a_linea)
        self.connect(self, SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.ir_a_linea)

    def actualizar_simbolos(self, simbolos):
        self.clear()

        if 'functions' in simbolos:
            funciones = QTreeWidgetItem(self)
            funciones.setText(0, self.tr("Funciones"))
            funciones.setIcon(0, QIcon(self.iconos['funcion']))
            funciones.setSelected(False)
            for f in list(simbolos['functions'].keys()):
                funcion = QTreeWidgetItem(funciones)
                funcion.setText(0, f)
                funcion.setToolTip(0, self.tooltip(
                    ['f', simbolos['functions'][f]]))
                funcion.setIcon(0, QIcon(self.iconos['funcion']))
            funciones.setExpanded(True)

        if 'variables' in simbolos:
            globales = QTreeWidgetItem(self)
            globales.setText(0, self.tr("Variables"))
            globales.setIcon(0, QIcon(self.iconos['global']))
            for v in list(simbolos['variables'].keys()):
                variable = QTreeWidgetItem(globales)
                variable.setText(0, v)
                variable.setIcon(0, QIcon(self.iconos['global']))
                variable.setToolTip(0,
                    self.tooltip(['v', simbolos['variables'][v]]))
            globales.setExpanded(True)

        if 'structs' in simbolos:
            structs = QTreeWidgetItem(self)
            structs.setText(0, self.tr("Structs"))
            structs.setIcon(0, QIcon(self.iconos['struct']))
            for s in list(simbolos['structs'].keys()):
                struct = QTreeWidgetItem(structs)
                struct.setText(0, s)
                struct.setIcon(0, QIcon(self.iconos['struct']))
                struct.setToolTip(0,
                    self.tooltip(['s', s, simbolos['structs'][s]]))
                for k in simbolos['structs'][s]:
                    for i in range(len(simbolos['structs'][s][k])):
                        miembro = QTreeWidgetItem(struct)
                        miembro.setText(0, simbolos['structs'][s][k][i])
                        miembro.setIcon(0, QIcon(self.iconos['miembro']))

                struct.setExpanded(True)
            structs.setExpanded(True)

        if 'enums' in simbolos:
            enums = QTreeWidgetItem(self)
            enums.setText(0, self.tr("Enums"))
            enums.setIcon(0, QIcon(self.iconos['enums']))
            for e in list(simbolos['enums'].keys()):
                enum = QTreeWidgetItem(enums)
                enum.setIcon(0, QIcon(self.iconos['enums']))
                enum.setText(0, e)
                for en in simbolos['enums'][e]:
                    for i in range(len(simbolos['enums'][e][en])):
                        enumerator = QTreeWidgetItem(enum)
                        enumerator.setText(0, simbolos['enums'][e][en][i])
                        enumerator.setIcon(0, QIcon(self.iconos['enumerator']))
                enum.setExpanded(True)
            enums.setExpanded(True)

    def tooltip(self, dato):
        tooltip = ""

        if dato[0] == 'f':
            tooltip = dato[1][1] + ", " + dato[1][0]
        if dato[0] == 'v':
            tooltip = ", " + dato[1]
        if dato[0] == 's':
            tooltip = ', ' + str(dato[-1].keys()[0])

        return tooltip

    def info_item(self, treeItem):
        nombre = treeItem.text(0)
        tooltip = str(treeItem.toolTip(0))
        info = nombre + ' ' + tooltip
        self.emit(SIGNAL("infoSimbolo(QString)"), info)

    def ir_a_linea(self, item):
        #FIXME: revisar en miembros y enums
        try:
            linea = int(item.toolTip(0).split(',')[-1])
            self.emit(SIGNAL("irALinea(int)"), linea)
        except:
            pass