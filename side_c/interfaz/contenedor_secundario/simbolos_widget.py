#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QTabWidget
import sys


class Tab(QTabWidget):

    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.ide = parent

        #self.simbWid = SimbolosWidget()
        self.agregar_widSimb()

    def agregar_tab(self, widget, nombre):
        self.addTab(widget, nombre)

    def agregar_widSimb(self):
        self.simbWid = SimbolosWidget()
        self.addTab(self.simbWid, self.trUtf8("Funciones"))

    def addTab(self, tab, n):
        QTabWidget.addTab(self, tab, n)


class SimbolosWidget(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)
        self.header().setHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setAnimated(True)
        self.simbActual = ('', {})

    def actualizar_simbolos(self, simb, nombre='', parent=None):
        if not parent:
            self.clear()
            self.simbActual = (nombre, simb)
            parent = self

        if 'funciones' in simb:
            gFuncion = ItemW(parent, [self.trUtf8("Funciones")])
            gFuncion.isClickable = False
            gFuncion.setExpanded(self.expandir_(gFuncion))


class ItemW(QTreeWidgetItem):

    def __init__(self, parent, nombre, linea=None):
        QTreeWidgetItem.__init__(self, parent, nombre)

        self.linea = linea
        self.isClickable = True
        self.esFuncion = False

app = QApplication(sys.argv)
w = SimbolosWidget()
w.show()
sys.exit(app.exec_())