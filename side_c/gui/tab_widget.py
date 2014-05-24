#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QIcon

from PyQt4.QtCore import SIGNAL

from side_c.gui.editor import editor
from side_c import recursos


class TabCentral(QTabWidget):

    def __init__(self, parent):
        QTabWidget.__init__(self, parent)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)
        self.parent = parent

        self.connect(self, SIGNAL("tabCloseRequested(int)"),
            self.removeTab)

    def agregar_tab(self, widget, titulo, index=None):

        if index is not None:
            insertar = self.insertTab(index, widget, titulo)
        else:
            insertar = self.addTab(widget, titulo)

        self.setCurrentIndex(insertar)
        widget.setFocus()

        return insertar

    def cerrar_tab(self):
        self.removeTab(self.currentIndex())

    def tab_es_modificado(self, v):
        """ Agrega ícono al tab si se hace una edición en el editor. """

        edit = self.currentWidget()
        #texto = self.tabBar().tabText(self.currentIndex())
        if isinstance(edit, editor.Editor) and v:
            edit.texto_modificado = True
            #texto = self.tabBar().tabText(self.currentIndex()) + ' **'
            #self.tabBar().setTabText(self.currentIndex(), texto)
            icon = QIcon(recursos.ICONOS['icono-tab'])

            self.tabBar().setTabIcon(self.currentIndex(), icon)