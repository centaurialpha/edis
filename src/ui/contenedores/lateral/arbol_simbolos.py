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

from PyQt4.QtCore import (
    SIGNAL,
    pyqtSignal
    )

from src import paths


class ArbolDeSimbolos(QTreeWidget):

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
        super(ArbolDeSimbolos, self).__init__()
        self.setObjectName("simbolos")
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.header().setStretchLastSection(False)
        self.header().setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)

        self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.ir_a_linea)
        self.connect(self, SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.ir_a_linea)

    def actualizar_simbolos(self, simbolos):
        if simbolos is None:
            QTreeWidgetItem(self, [self.tr('ctags no está instalado.')])
            return
        self.clear()

        if 'variable' in simbolos:
            variables = Item(self, [self.tr('Variables')])
            variables.clickeable = False
            for v in simbolos['variable']:
                variable = Item(variables, [v.get('nombre')])
                linea = v['linea']
                variable.linea = linea
                variable.setIcon(0, QIcon(self.iconos['global']))
            variables.setExpanded(True)

        if 'function' in simbolos:
            funciones = Item(self, [self.tr('Funciones')])
            funciones.clickeable = False
            for f in simbolos['function']:
                funcion = Item(funciones, [f.get('nombre')])
                linea = f['linea']
                funcion.linea = linea
                funcion.setIcon(0, QIcon(self.iconos['funcion']))
            funciones.setExpanded(True)

        if 'struct' in simbolos:
            structs = Item(self, [self.tr('Estructuras')])
            structs.clickeable = False
            for s in simbolos['struct']:
                struct = Item(structs, [s.get('nombre')])
                linea = s['linea']
                struct.linea = linea
                struct.setIcon(0, QIcon(self.iconos['struct']))
            structs.setExpanded(True)

        if 'member' in simbolos:
            miembros = Item(self, [self.tr('Miembros')])
            miembros.clickeable = False
            for m in simbolos['member']:
                nombre = m['nombre'] + ' [' + m['padre'] + ']'
                miembro = Item(miembros, [nombre])
                miembro.setIcon(0, QIcon(self.iconos['miembro']))
                linea = m['linea']
                miembro.linea = linea

            miembros.setExpanded(True)

    def ir_a_linea(self, item):
        if item.clickeable:
            self._ir_a_linea.emit(int(item.linea) - 1)

    def closeEvent(self, e):
        super(ArbolDeSimbolos, self).closeEvent(e)
        #FIXME: emitir señal de cerrado para hacer dock


class Item(QTreeWidgetItem):

    def __init__(self, parent, nombre):
        QTreeWidgetItem.__init__(self, parent, nombre)
        self.linea = None
        self.clickeable = True