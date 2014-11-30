# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import os

# Módulos QtGui
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QIcon

# Módulos QtCore
from PyQt4.QtCore import QDir
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

# Módulos EDIS
from src.helpers import manejador_de_archivo
from src import recursos
from src.ui import tab_widget
from src.ui.editor import (
    editor,
    highlighter_,
    #acciones_
    )

__instanciaContenedorMain = None


# Singleton
def ContenedorMain(*args, **kw):
    global __instanciaContenedorMain
    if __instanciaContenedorMain is None:
        __instanciaContenedorMain = __ContenedorMain(*args, **kw)
    return __instanciaContenedorMain


class __ContenedorMain(QSplitter):
    """ Splitter principal que contiene el editor. """

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)

        self.parent = parent
        self.tab = tab_widget.TabCentral(self)
        self.setAcceptDrops(True)
        self.addWidget(self.tab)
        self.setSizes([1, 1])
        self.setFixedSize(0, 450)
        highlighter_.re_estilo(recursos.NUEVO_TEMA)
        self.connect(self.tab, SIGNAL("currentChanged(int)"),
            self.tab_actual_cambiado)
        self.connect(self.tab, SIGNAL("saveActualEditor()"),
            self.guardar_archivo)
        #self.connect(self.tab, SIGNAL("currentChanged(int)"),
            #self.tab_actual_cambiado)
        self.tab.boton.accionCrear.triggered.connect(
            lambda: self.agregar_editor(''))
        self.connect(self.tab,
            SIGNAL("recentTabsModified(QStringList)"),
            self.archivos_recientes_cambiado)
        self.connect(self.tab, SIGNAL("archivoCerrado(int)"),
            self.cerrar_item_lista)
        self.connect(self, SIGNAL("abriendoArchivos(QStringList)"),
            self.cargar_archivo_lista)

        tecla = Qt.Key_1
        for i in range(10):
            atajo = TabAtajos(QKeySequence(Qt.ALT + tecla), self.parent, i)
            tecla += 1
            atajo.activated.connect(self.cambiar_indice_de_tab)

    def archivos_recientes_cambiado(self, archivos):
        self.emit(SIGNAL("recentTabsModified(QStringList)"), archivos)

    def agregar_editor(self, nombre_archivo=""):
        """ Agrega un QPlainTextEdit
            @nombre_archivo: texto QString para el nombre del documento.
            por defecto False.
        """

        editorWidget = editor.crear_editor(nombre_archivo=nombre_archivo)
        if not nombre_archivo:
            nombre_tab = "Nuevo archivo"
            icono = False
        else:
            nombre_tab = manejador_de_archivo._nombreBase(nombre_archivo)
            # Extensión del archivo
            ext = nombre_tab.strip('.')[-1]
            if ext == 'c':
                icono = recursos.ICONOS['c']
            elif ext == 'h':
                icono = recursos.ICONOS['h']
            else:
                icono = False

        indice = self.agregar_tab(editorWidget, icono, nombre_tab)
        self.tab.setTabToolTip(indice,
            QDir.toNativeSeparators(nombre_archivo))
        self.connect(editorWidget, SIGNAL("archivo_guardado(PyQt_PyObject)"),
            self.editor_es_guardado)
        self.connect(editorWidget, SIGNAL("openDropFile(QString)"),
            self.abrir_archivo)
        self.emit(SIGNAL("fileOpened(QString)"), nombre_archivo)
        self.connect(editorWidget, SIGNAL("cursorPositionChanged(int, int)"),
            self._posicion_del_cursor)
        self.connect(editorWidget, SIGNAL("archivo_modificado(bool)"),
            self.editor_es_modificado)
        self.connect(editorWidget, SIGNAL("accion_undo(PyQt_PyObject)"),
            self.editor_es_guardado)

        return editorWidget

    def _editor_keyPressEvent(self, evento):
        self.emit(SIGNAL("editorKeyPressEvent(QEvent)"), evento)

    def editor_es_modificado(self, v):
        self.tab.tab_es_modificado(v)
        self.parent.barra_de_estado.archivo_modificado.modificado(v)

    def editor_es_guardado(self, editorW=None):
        self.tab.tab_guardado(editorW)
        self.emit(SIGNAL("actualizarSimbolos(QString)"), editorW.iD)

    def check_tabs_sin_guardar(self):
        return self.tab.check_tabs_sin_guardar()

    def devolver_archivos_sin_guardar(self):
        """ Retorna una lista con archivos sin guardar. """

        return self.tab.devolver_archivos_sin_guardar()

    def get_archivos(self):
        archivos = []
        for i in range(self.tab.count()):
            editorW = self.tab.widget(i)
            if isinstance(editorW, editor.Editor):
                archivos.append(editorW._id.split('/')[-1])

    def agregar_tab(self, widget, icono, nombre_tab, nAbierta=True):
        """ Se llama al método agregar_tab de la clase TabCentral
        retorna QTabWidget.
        """

        return self.tab.agregar_tab(widget, icono, nombre_tab)

    def devolver_widget_actual(self):
        """ Retorna QTabWidget actual. """

        return self.tab.currentWidget()

    def devolver_editor_actual(self):
        """ Si el widget es una instancia de QPlainTextEdit se lo retorna,
        de lo contrario se retorna None.
        """

        e = self.tab.currentWidget()
        if isinstance(e, editor.Editor):
            return e
        else:
            return None

    def cargar_archivo_lista(self, archivos):
        self.parent.lateral.file_navigator.cargar_archivos(archivos)

    def cerrar_item_lista(self, indice):
        self.parent.lateral.file_navigator.borrar_item(indice)

    def deshacer(self):
        self.get_archivos()
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

    def indentar_mas(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.indentar_mas()

    def indentar_menos(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.indentar_menos()

    def actualizar_margen_editor(self):
        for i in range(self.tab.count()):
            widget = self.tab.widget(i)
            #if type(widget) is editor.Editor:
            if isinstance(widget, editor.Editor):
                widget.actualizar_margen_linea()

    def setFocus(self):
        w = self.devolver_widget_actual()
        if w:
            w.setFocus()

    def _posicion_del_cursor(self, linea, columna):
        self.emit(SIGNAL("cursorPositionChanged(int, int)"), linea, columna)

    def cerrar_tab(self):
        """ Se llama al método removeTab de QTabWidget. """

        self.tab.cerrar_tab()

    def cerrar_todo(self):
        self.tab.cerrar_todo()

    def cerrar_excepto_actual(self):
        self.tab.cerrar_excepto_actual()

    def actual_widget(self):
        return self.tab.currentWidget()

    def tab_actual_cambiado(self, indice):
        if self.tab.widget(indice):
            self.emit(SIGNAL("currentTabChanged(QString)"),
                self.tab.widget(indice)._id)

    def cambiar_nombre_de_tab(self, aidi, nuevoId):
        indice_tab = self.tab.esta_abierto(aidi)
        if indice_tab is not False:
            w = self.tab.w(indice_tab)
            TAB = self.tab

        nombre_de_tab = manejador_de_archivo._nombreBase(nuevoId)
        TAB.cambiar_nombre_de_tab(indice_tab, nombre_de_tab)
        w.iD = nuevoId

    def cambiar_indice_de_tab(self):
        Weditor = self.parent.contenedor_principal.devolver_editor_actual()
        if Weditor is not None and Weditor.hasFocus():
            contenedor = self.parent.contenedor_principal.tab
        else:
            return None
        obj = self.sender()
        if obj.indice < contenedor.count():
            contenedor.setCurrentIndex(obj.indice)

    def abrir_archivos(self, archivos):
        for data in archivos:
            if not data:
                return
            self.abrir_archivo(data[0])

    def abrir_archivo(self, nombre=''):
        extension = recursos.EXTENSIONES  # Filtro
        nombre = unicode(nombre)

        if not nombre:

            direc = os.path.expanduser("~")
            Weditor = self.devolver_editor_actual()
            # Para recordar la última carpeta
            if Weditor is not None and Weditor._id:
                direc = manejador_de_archivo.devolver_carpeta(Weditor._id)
            nombres = list(QFileDialog.getOpenFileNames(self,
            self.trUtf8("Abrir archivo"), direc, extension))

        else:
            nombres = [nombre]
        if not nombres:
            return

        for nombre in nombres:
            nombre = unicode(nombre)
            #contenido = self.leer_contenido_archivo(nombre)
            if not self.abierto(nombre):
                self.tab.no_esta_abierto = False
                contenido = manejador_de_archivo.leer_contenido_de_archivo(
                    nombre)
                editorW = self.agregar_editor(nombre)
                #editorW.setPlainText(contenido.decode('utf-8'))
                editorW.texto = contenido
                editorW.iD = nombre

                # Reemplaza tabulaciones por espacios en blanco
                #editorW.tabulaciones_por_espacios_en_blanco()
                editorW.nuevo_archivo = False
            else:
                self.mover_abierto(nombre)
        self.emit(SIGNAL("currentTabChanged(QString)"), nombre)
        self.emit(SIGNAL("abriendoArchivos(QStringList)"), nombres)
        self.tab.no_esta_abierto = True

    def abierto(self, archivo):
        """ Comprueba si el archivo ya esta abierto. """

        t = self.tab.abierto(archivo)
        if t is not False:
            return t
        return False

    def mover_abierto(self, archivo):
        if self.tab.abierto(archivo) != -1:
            self.tab.mover_abierto(archivo)
        self.tab.currentWidget().setFocus()
        self.emit(SIGNAL("currentTabChanged(QString)"), archivo)

    def get_documentos_abiertos(self):
        return [self.tab.devolver_documentos_para_reabrir()]

    def guardar_archivo(self, editorW=None):
        if not editorW:
            editorW = self.devolver_editor_actual()
            if not editorW:
                return False

        try:
            #FIXME: Arreglar todo esto
            editorW.guardado_actualmente = True

            if editorW.nuevo_archivo or \
            not manejador_de_archivo.permiso_de_escritura(editorW._id):
                return self.guardar_archivo_como()

            nombre = editorW._id
            #carpeta_de_archivo = manejador_de_archivo.devolver_carpeta(nombre)
            self.emit(SIGNAL("beforeFileSaved(QString)"), nombre)
            #acciones_.quitar_espacios_en_blanco(editorW)
            contenido = editorW.texto
            manejador_de_archivo.escribir_archivo(nombre, contenido)
            editorW.iD = nombre

            self.emit(SIGNAL("archivoGuardado(QString)"), self.tr(
                "Guardado: %1").arg(nombre))

            editorW.guardado()

            return editorW._id
        except:
            editorW.guardado_actualmente = False
            return False

    def guardar_archivo_como(self):
        editorW = self.devolver_editor_actual()
        if not editorW:
            return False

        direc = os.path.expanduser("~")

        try:
            editorW.guardado_actualmente = True
            nombre = str(QFileDialog.getSaveFileName(
                self.parent, self.tr("Guardar"), direc,
                '(*.c);;(*.h);;(*.*)'))
            if not nombre:
                return False

            #acciones_.quitar_espacios_en_blanco(editorW)
            nombre = manejador_de_archivo.escribir_archivo(
                nombre, editorW.texto)
            ext = manejador_de_archivo._nombreBase(nombre)[-1]
            if ext == 'c':
                icono = recursos.ICONOS['c']
            else:
                icono = recursos.ICONOS['h']
            self.tab.setTabText(self.tab.currentIndex(),
                manejador_de_archivo._nombreBase(nombre))
            self.tab.setTabIcon(self.tab.currentIndex(),
                QIcon(icono))
            editorW.iD = nombre

            # Señal de guardado para la barra de estado
            self.emit(SIGNAL("archivoGuardado(QString)"),
                self.tr("Guardado: %1").arg(nombre))
            self.emit(SIGNAL("guardadoList(QString)"),
                editorW._id)
            editorW.guardado()

            return editorW._id

        except:
            editorW.guardado_actualmente = False
            self.tab.setTabText(self.tab.currentIndex(),
                self.trUtf8("Nuevo archivo"))
        return False

    def guardar_todo(self):

        for i in range(self.tab.count()):
            editorW = self.tab.widget(i)

            if isinstance(editorW, editor.Editor):
                self.guardar_archivo(editorW)

    def guardar_seleccionado(self, nombre):
        for i in range(self.tab.count()):
            editorW = self.tab.widget(i)

            if isinstance(editorW, editor.Editor):
                if editorW._id == nombre:
                    self.guardar_archivo(editorW)

    def resetear_flags_editor(self):
        for i in range(self.tab.count()):
            widget = self.tab.widget(i)
            if isinstance(widget, editor.Editor):
                widget.set_flags()


class TabAtajos(QShortcut):

    def __init__(self, tecla, parent, indice):
        super(TabAtajos, self).__init__(tecla, parent)
        self.indice = indice