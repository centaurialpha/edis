#-*- coding: utf-8 -*-
import os

from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMessageBox
#from PyQt4.QtGui import QApplication

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QTextStream
#from PyQt4.QtCore import Qt

from side_c import recursos
from side_c.interfaz import tab_widget
#from side_c.interfaz import barra_de_estado
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
        self.connect(editorWidget, SIGNAL("fileSaved(QPlainTextEdit)"),
            self.editor_es_guardado)
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

    def editor_es_guardado(self, e=None):
        self.tab_actual.tab_es_guardado(e)
        self.emit(SIGNAL("updateLocator(QString)"), e.ID)

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
            if not self.esta_abierto(nombre):
                self.tab_actual.no_esta_abierto = False
                contenido = self.leer_contenido_archivo(nombre)
                eW = self.agregar_editor(nombre, tabIndex=tabIndex)

                eW.setPlainText(contenido)
                eW.ID = nombre

                self.emit(SIGNAL("currentTabChanged(QString)"), nombre)
        except:
            pass
        self.tab_actual.no_esta_abierto = True

    def esta_abierto(self, nombre):
        return self.tab_principal._esta_abierto(nombre) != -1

    def mover_tab(self, nombre):
        if self.tab_principal._esta_abierto(nombre) != -1:
            self.tab_principal._mover_tab(nombre)
            self.tab_actual = self.tab_principal

        self.tab_actual.currentWidget().setFocus()
        self.emit(SIGNAL("currentTabChangd(QString)"), nombre)

    def guardar_archivo(self, editorW=None):
        if not editorW:
            editorW = self.devolver_editor_actual()
        if not editorW:
            return False

        try:
            if editorW.nuevo_archivo:
                print "NUEVO"
                return self.guardar_archivo_como()

            nombre = editorW.ID

            contenido = editorW.devolver_texto()
            salidaF = QFile(nombre)

            stream = QTextStream(salidaF)
            stream.setCodec('utf-8')
            enc_s = stream.codec().fromUnicode(contenido)
            salidaF.write(enc_s)
            salidaF.flush()
            salidaF.close()
            editorW.ID = nombre
            self.emit(SIGNAL("fileSaved(QString)"), self.tr("Guardado"))

            print "Guardado!"

            editorW._guardado()
            return True
        except:
            pass
        return False

    def guardar_archivo_como(self):
        CODEC = 'utf-8'

        editorW = self.devolver_editor_actual()
        if not editorW:
            return False

        try:
            nombre = QFileDialog.getSaveFileName(
                self.parent, self.tr("Guardar"), QDir.currentPath(), '(*.*)')
            if not nombre:
                return False

            salidaF = QFile(nombre)
            if not salidaF.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self,
                    "Guardar", "No se escribio en %s: %s" % (
                        nombre, salidaF.errorString()))
                return False

            contenido = editorW.devolver_texto()

            stream = QTextStream(salidaF)
            stream.setCodec(CODEC)
            enc_s = stream.codec().fromUnicode(contenido)
            salidaF.write(enc_s)
            salidaF.flush()
            salidaF.close()

            self.tab_actual.setTabText(self.tab_actual.currentIndex(),
                self._nombreBase(nombre))
            editorW.ID = nombre
            self.emit(SIGNAL("fileSaved(QString)"),
                self.tr("Guardado"))
            editorW._guardado()
            print "Guardado como!"
            return True

        except:
            pass
        return False

    def leer_contenido_archivo(self, archivo):
        """ Recibe (archivo), lee y lo retorna. """
        import codecs

        with codecs.open(archivo, 'r', 'utf-8') as f:
            contenido = f.read()

        return contenido

    def permiso_de_escritura(self, archivo):
        return os.access(archivo, os.W_OK)