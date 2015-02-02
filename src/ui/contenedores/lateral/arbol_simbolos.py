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
    QIcon,
    QDockWidget,
    )

from PyQt4.QtCore import pyqtSignal

from src.ectags import ectags
from src import paths
from src.ui.edis_main import EDIS


class ArbolDeSimbolos(QDockWidget):

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
        QDockWidget.__init__(self)
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
        self.tree.itemClicked[QTreeWidgetItem, int].connect(self.ir_a_linea)
        self.tree.itemActivated[QTreeWidgetItem, int].connect(self.ir_a_linea)

        EDIS.cargar_lateral("simbolos", self)

    def actualizar_simbolos(self, archivo):
        #FIXME: mover esto
        self.ctags = ectags.Ctags()
        tag = self.ctags.run_ctags(archivo)
        simbolos = self.ctags.parser(tag)
        self._actualizar_simbolos(simbolos)

    def _actualizar_simbolos(self, simbolos):
        if simbolos is None:
            QTreeWidgetItem(self.tree, [self.tr('ctags no está instalado.')])
            return

        # Limpiar
        self.tree.clear()

        if 'variable' in simbolos:
            variables = Item(self.tree, [self.tr('Variables')])
            variables.clickeable = False
            for v in simbolos['variable']:
                variable = Item(variables, [v.get('nombre')])
                linea = v['linea']
                variable.linea = linea
                variable.setIcon(0, QIcon(self.iconos['global']))
            variables.setExpanded(True)

        if 'function' in simbolos:
            funciones = Item(self.tree, [self.tr('Funciones')])
            funciones.clickeable = False
            for f in simbolos['function']:
                funcion = Item(funciones, [f.get('nombre')])
                linea = f['linea']
                funcion.linea = linea
                funcion.setIcon(0, QIcon(self.iconos['funcion']))
            funciones.setExpanded(True)

        if 'struct' in simbolos:
            structs = Item(self.tree, [self.tr('Estructuras')])
            structs.clickeable = False
            for s in simbolos['struct']:
                struct = Item(structs, [s.get('nombre')])
                linea = s['linea']
                struct.linea = linea
                struct.setIcon(0, QIcon(self.iconos['struct']))
            structs.setExpanded(True)

        if 'member' in simbolos:
            miembros = Item(self.tree, [self.tr('Miembros')])
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

    def showEvent(self, evento):
        """ Fija el ancho """

        super(ArbolDeSimbolos, self).showEvent(evento)
        self.setFixedWidth(256)


class Item(QTreeWidgetItem):

    def __init__(self, parent, nombre):
        QTreeWidgetItem.__init__(self, parent, nombre)
        self.linea = None
        self.clickeable = True


simbolos = ArbolDeSimbolos()