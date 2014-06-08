#-*- coding: utf-8 -*-
import os

from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import SIGNAL

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
        else:
            nombre_tab = self._nombreBase(nombre_archivo)

        self.agregar_tab(editorWidget, nombre_tab, tabIndex=tabIndex)

        self.connect(editorWidget, SIGNAL("modificationChanged(bool)"),
            self.editor_es_modificado)
        self.connect(editorWidget, SIGNAL("openDropFile(QString)"),
            self.abrir_archivo)
        self.emit(SIGNAL("fileOpened(QString)"), nombre_archivo)

        return editorWidget

    def _nombreBase(self, nombre):
        if nombre.endswith(os.path.sep):
            nombre = nombre[:-1]
        return os.path.basename(nombre)

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

    def agregar_tab(self, widget, nombre_tab, tabIndex=None, nAbierta=True):
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

    def abrir_archivo(self, nombre='', cursor=0, tabIndex=None):
        extension = recursos.EXTENSIONES  # Filtro

        if not nombre:
            direc = os.path.expanduser("~")

            nombres = list(QFileDialog.getOpenFileNames(self,
            self.tr("Abrir archivo"), direc, extension))
        else:
            nombres = [nombre]
        if not nombres:
            return

        for nombre in nombres:
            nombre = str(nombre)
            self._abrir_archivo(nombre, cursor, tabIndex)

    def _abrir_archivo(self, nombre='', cursor=0, tabIndex=None):
        try:
            contenido = self.leer_contenido_archivo(nombre)
            eW = self.agregar_editor(nombre, tabIndex=tabIndex)

            eW.setPlainText(contenido)
            eW.ID = nombre
        except:
            #print "Prueba"
            pass

    def esta_abierto(self, nombre):
        return self.tab_principal._esta_abierto(nombre) != -1

    def mover_tab(self, nombre):
        if self.tab_principal._esta_abierto(nombre) != -1:
            self.tab_principal._mover_tab(nombre)
            self.tab_actual = self.tab_principal

        self.tab_actual.currentWidget().setFocus()
        self.emit(SIGNAL("currentTabChangd(QString)"), nombre)

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