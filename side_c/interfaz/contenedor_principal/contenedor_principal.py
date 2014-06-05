#-*- coding: utf-8 -*-
import os

from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog

#from PyQt4.QtCore import QString
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QTextStream

from side_c import recursos
from side_c.interfaz import tab_widget
from side_c.interfaz.editor import editor

__instanciaContenedorMain = None


# Singleton
def ContenedorMain(*args, **kw):
    global __instanciaContenedorMain
    if __instanciaContenedorMain is None:
        __instanciaContenedorMain = __ContenedorMain(*args, **kw)
    return __instanciaContenedorMain


class __ContenedorMain(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)
        self.parent = parent
        self.tab_principal = tab_widget.TabCentral(self)
        self.setAcceptDrops(True)
        self.addWidget(self.tab_principal)
        self.setSizes([1, 1])
        self.setFixedSize(0, 500)
        self.tab_actual = self.tab_principal

    def agregar_editor(self, nombre_archivo="", tabIndex=None):
        editorWidget = editor.crear_editor(nombre_archivo=nombre_archivo)

        if not nombre_archivo:
            nombre_tab = "Nuevo archivo"

        self.agregar_tab(editorWidget, nombre_tab, tabIndex=tabIndex)

        self.connect(editorWidget, SIGNAL("modificationChanged(bool)"),
            self.editor_es_modificado)

        return editorWidget

    def deshacer(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.undo()

    def rehacer(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.redo()

    def cortar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.cut()

    def copiar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.copy()

    def pegar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.paste()

    def seleccionar_todo(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.selectAll()

    def borrar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.clear()

    def devolver_widget_actual(self):
        return self.tab_actual.currentWidget()

    def devolver_editor_actual(self):
        e = self.tab_actual.currentWidget()
        if isinstance(e, editor.Editor):
            return e
        else:
            return None

    def actualizar_margen_editor(self):
        for i in range(self.tab_principal.count()):
            widget = self.tab_principal.widget(i)
            #if type(widget) is editor.Editor:
            if isinstance(widget, editor.Editor):
                widget.actualizar_margen_linea()

    def setFocus(self):
        w = self.devolver_widget_actual()
        if w:
            w.setFocus()

    def agregar_tab(self, widget, nombre_tab, tabIndex=None):
        return self.tab_actual.agregar_tab(widget, nombre_tab, index=tabIndex)

    def cerrar_tab(self):
        """ Se llama al método removeTab de QTabWidget. """

        self.tab_actual.cerrar_tab()

    def cerrar_todo(self):
        self.tab_actual.cerrar_todo()

    def cerrar_excepto_actual(self):
        self.tab_actual.cerrar_excepto_actual()

    def actual_widget(self):
        return self.tab_actual.currentWidget()

    def editor_es_modificado(self, v=True):
        self.tab_actual.tab_es_modificado(v)

    def abrir_archivo(self, nombre='', tabIndex=None, cursor=0):
        extension = ';;'.join(
            ['(*%s)' % ex for ex in
            recursos.EXTENSIONES + ['.*', '']])

        if not nombre:
            directorio = os.path.expanduser("~")
            editorW = self.devolver_editor_actual()

            nombres = unicode(QFileDialog.getOpenFileName(
                self, self.tr("Abrir archivo"),
                directorio, extension))

            contenido = self.leer_contenido_archivo(nombres)
            editorW = self.agregar_editor(nombre, tabIndex)

            editorW.setPlainText(contenido)
            editorW.ID = nombre
            editorW.posicion_cursor(cursor)

            index = self.tab_actual.currentIndex()
            self.tab_actual.setTabText(index, nombres)

    def guardar_archivo(self, editorW=None):
        pass

    def guardar_archivo_como(self):
        pass

    def leer_contenido_archivo(self, archivo):
        """ Recibe (archivo), lee y lo retorna. """
        import codecs

        with codecs.open(archivo, 'r', 'utf-8') as f:
            contenido = f.read()

        return contenido

    def permiso_de_escritura(self, archivo):
        return os.access(archivo, os.W_OK)