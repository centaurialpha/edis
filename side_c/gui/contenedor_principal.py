#-*- coding: utf-8 -*-

from PyQt4.QtGui import QSplitter

from PyQt4.QtCore import SIGNAL

from side_c.gui.editor import editor

from side_c.gui import tab_widget


class ContenedorMain(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)
        self.parent = parent
        self.tab_principal = tab_widget.TabCentral(self)
        self.setAcceptDrops(True)
        self.addWidget(self.tab_principal)
        self.setSizes([1, 1])
        self.setFixedSize(0, 450)
        self.tab_actual = self.tab_principal

    def agregar_editor(self, nombre_archivo="", tabIndex=None):
        editorWidget = editor.crear_editor(nombre_archivo=nombre_archivo)

        if not nombre_archivo:
            nombre_tab = "Nuevo archivo"

        self.agregar_tab(editorWidget, nombre_tab, tabIndex=tabIndex)

        self.connect(editorWidget, SIGNAL("modificationChanged(bool)"),
            self.editor_es_modificado)

        return editorWidget

    def agregar_tab(self, widget, nombre_tab, tabIndex=None):
        return self.tab_actual.agregar_tab(widget, nombre_tab, index=tabIndex)

    def cerrar_tab(self):
        """ Se llama al método removeTab de QTabWidget. """

        self.tab_actual.cerrar_tab()

    def actual_widget(self):
        return self.tab_actual.currentWidget()

    def editor_es_modificado(self, v=True):
        self.tab_actual.tab_es_modificado(v)