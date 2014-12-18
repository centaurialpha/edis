# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

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

from src import recursos


class ArbolDeSimbolos(QTreeWidget):
    iconos = {
        'clase': recursos.ICONOS['class'],
        'funcion': recursos.ICONOS['funcion'],
        'struct': recursos.ICONOS['struct'],
        'miembro': recursos.ICONOS['miembro'],
        'global': recursos.ICONOS['variable'],
        'enumerator': recursos.ICONOS['enumerator'],
        'enums': recursos.ICONOS['enums']
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
            self.info_item)
        self.connect(self, SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.info_item)
        self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.ir_a_linea)
        self.connect(self, SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.ir_a_linea)

    def actualizar_simbolos(self, simbolos):
        self.clear()

        if 'globals' in simbolos:
            globalss = Item(self, [self.tr("Variables")])
            globalss.clicked = False
            globalss.setIcon(0, QIcon(self.iconos['global']))
            for v in list(simbolos['globals'].keys()):
                variable = Item(globalss, [v])
                variable.line = simbolos['globals'][v]
                variable.setIcon(0, QIcon(self.iconos['global']))
            globalss.setExpanded(True)

        if 'classes' in simbolos:
            classs = Item(self, [self.tr("Clases")])
            classs.clicked = False
            classs.setIcon(0, QIcon(self.iconos['clase']))
            for c in list(simbolos['classes'].keys()):
                clase = Item(classs, [c])
                clase.line = simbolos['classes'][c][0]
                clase.setIcon(0, QIcon(self.iconos['clase']))
                if simbolos['classes'][c][1]['attributes']:
                    att = Item(clase, [self.tr("Atributos")])
                    att.clicked = False
                    att.setIcon(0, QIcon(self.iconos['miembro']))
                    for at in simbolos['classes'][c][1]['attributes']:
                        atr = Item(att, [at])
                        atr.line = simbolos['classes'][c][1]['attributes'][at]
                        atr.setIcon(0, QIcon(self.iconos['miembro']))
                    att.setExpanded(True)
                if simbolos['classes'][c][2]['methods']:
                    mett = Item(clase, [self.trUtf8("Métodos")])
                    mett.clicked = False
                    mett.setIcon(0, QIcon(self.iconos['funcion']))
                    for m in simbolos['classes'][c][2]['methods']:
                        met = Item(mett, [m])
                        met.line = simbolos['classes'][c][2]['methods'][m]
                        met.setIcon(0, QIcon(self.iconos['funcion']))
                    mett.setExpanded(True)
                    clase.setExpanded(True)
                classs.setExpanded(True)

        if 'structs' in simbolos:
            structs = Item(self, [self.tr("Estructuras")])
            structs.clicked = False
            structs.setIcon(0, QIcon(self.iconos['struct']))
            for s in list(simbolos['structs'].keys()):
                struct = Item(structs, [s])
                struct.line = simbolos['structs'][s][0]
                struct.setIcon(0, QIcon(self.iconos['struct']))
                for m in simbolos['structs'][s][1]['members']:
                    member = Item(struct, [m])
                    member.line = simbolos['structs'][s][1]['members'][m]
                    member.setIcon(0, QIcon(self.iconos['miembro']))
                struct.setExpanded(True)
            structs.setExpanded(True)
        if 'functions' in simbolos:
            functions = Item(self, [self.tr("Funciones")])
            functions.clicked = False
            functions.setIcon(0, QIcon(self.iconos['funcion']))
            for f in list(simbolos['functions'].keys()):
                function = Item(functions, [f])
                function.line = simbolos['functions'][f]
                function.setIcon(0, QIcon(self.iconos['funcion']))
            functions.setExpanded(True)

        if 'enums' in simbolos:
            enums = Item(self, [self.tr("Enums")])
            enums.clicked = False
            enums.setIcon(0, QIcon(self.iconos['enums']))
            for e in list(simbolos['enums'].keys()):
                enum = Item(enums, [e])
                enum.line = simbolos['enums'][e][0]
                enum.setIcon(0, QIcon(self.iconos['enums']))
                for enu in simbolos['enums'][e][1]['enumerators']:
                    enumerator = Item(enum, [enu])
                    enumerator.line = \
                                    simbolos['enums'][e][1]['enumerators'][enu]
                    enumerator.setIcon(0, QIcon(self.iconos['enumerator']))
                enum.setExpanded(True)
            enums.setExpanded(True)

    def tooltip(self, dato):
        pass

    def info_item(self, treeItem):
        pass

    def ir_a_linea(self, item):
        if item.clicked:
            self.emit(SIGNAL("irALinea(int)"), int(item.line))


class Item(QTreeWidgetItem):

    def __init__(self, parent, name):
        QTreeWidgetItem.__init__(self, parent, name)
        self.__line = None
        self.clicked = True

    def set_line(self, line):
        self.__line = line

    def get_line(self):
        return self.__line

    line = property(get_line, set_line)