# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QFileDialog,
    )

from PyQt4.QtCore import (
    SIGNAL,
    QFileInfo,
    pyqtSignal
    )

from src.helpers import (
    manejador_de_archivo,
    logger
    )
from src import recursos
from src.ui.editor import (
    editor,
    stack
    )
from src.ui.edis_main import EDIS
from src.ui.widgets import busqueda
from src.ui.contenedores import selector
from src.ui.dialogos import (
    dialogo_propiedades,
    dialogo_log
    )

# Logger
log = logger.edisLogger("contenedores.principal")


class EditorContainer(QWidget):

    archivo_cambiado = pyqtSignal(['QString'])
    posicion_cursor = pyqtSignal(int, int, int)

    def __init__(self, edis=None):
        QWidget.__init__(self, edis)
        self.setAcceptDrops(True)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.stack = stack.StackWidget(self)
        vbox.addWidget(self.stack)

        self.instalar_signals()
        EDIS.cargar_componente("principal", self)

    def instalar_signals(self):
        self.connect(self.stack, SIGNAL("Guardar_Editor_Actual()"),
                    self.guardar_archivo)
        #self.connect(self.widget_actual.stack, SIGNAL("currentChanged(int)"),
                    #self.cambiar_widget)
        #self.connect(self.widget_actual, SIGNAL("archivo_modificado(bool)"),
                    #self._archivo_modificado)

    def _archivo_modificado(self, valor):
        self.emit(SIGNAL("archivo_modificado(bool)"), valor)

    def __archivo_guardado(self, weditor):
        self.emit(SIGNAL("actualizarSimbolos(QString)"), weditor.iD)

    def cambiar_widget(self, indice):
        self.stack.cambiar_widget(indice)
        weditor = self.devolver_editor()
        if weditor is not None:
            self.archivo_cambiado.emit(weditor.iD)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        weditor = editor.crear_editor(nombre)
        self.agregar_widget(weditor)
        weditor.modificationChanged[bool].connect(self.stack.editor_modificado)
        weditor.cursorPositionChanged[int, int].connect(self.actualizar_cursor)
        weditor.archivo_guardado.connect(self.__archivo_guardado)
        weditor.setFocus()
        return weditor

    def abrir_archivo(self, nombre=""):
        if not nombre:
            carpeta = os.path.expanduser("~")
            editor_widget = self.widget_actual()
            if editor_widget and editor_widget.iD:
                carpeta = self.__ultima_carpeta_visitada(editor_widget.iD)
            archivos = QFileDialog.getOpenFileNames(self,
                            self.trUtf8("Abrir archivo"), carpeta,
                            recursos.EXTENSIONES)
        else:
            archivos = [nombre]
        for archivo in archivos:
            if not self.__archivo_abierto(archivo):
                self.stack.no_esta_abierto = False
                contenido = manejador_de_archivo.leer_contenido_de_archivo(
                            archivo)
                nuevo_editor = self.agregar_editor(archivo)
                nuevo_editor.texto = contenido
                nuevo_editor.iD = archivo
                self.archivo_cambiado.emit(archivo)

        self.stack.no_esta_abierto = True

    def __ultima_carpeta_visitada(self, path):
        """ Devuelve la última carpeta a la que se accedió """

        return QFileInfo(path).absolutePath()

    def __archivo_abierto(self, archivo):
        """
        Retorna True si un archivo ya esta abierto,
        False en caso contrario

        """

        editores = self.stack.editores
        for editor_widget in editores:
            if editor_widget.iD == archivo:
                log.warning(
                    "El archivo %s ya esta abierto", archivo)
                return True
        return False

    def agregar_widget(self, widget):
        """ Agrega @widget al stacked """

        self.stack.agregar_widget(widget)

    def eliminar_widget(self, widget):
        """ Elimina el @widget del stacked """

        self.stack.removeWidget(widget)

    def widget_actual(self):
        """ Widget actual """

        return self.stack.widget_actual

    def indice_actual(self):
        return self.stack.indice_actual

    def devolver_editor(self):
        """ Devuelve el Editor si el widget actual es una instancia de él,
        de lo contrario devuelve None. """

        widget = self.widget_actual()
        if isinstance(widget, editor.Editor):
            return widget
        return None

    def cerrar_archivo(self):
        self.stack.cerrar()

    def cerrar_todo(self):
        self.stack.cerrar_todo()

    def cerrar_demas(self):
        self.stack.cerrar_demas()

    def selector(self):
        if self.devolver_editor() is not None:
            selector_ = selector.Selector(self)
            selector_.show()

    def guardar_archivo(self, weditor=None):
        #FIXME: Controlar con try-except
        if not weditor:
            weditor = self.devolver_editor()
            if not weditor:
                return False

        if weditor.nuevo_archivo:
            return self.guardar_archivo_como(weditor)
        nombre_archivo = weditor.iD
        codigo_fuente = weditor.texto
        manejador_de_archivo.escribir_archivo(nombre_archivo, codigo_fuente)
        weditor.iD = nombre_archivo
        weditor.guardado()

    def guardar_archivo_como(self, weditor):
        #FIXME: Controlar con try-except
        carpeta = os.path.expanduser("~")
        nombre_archivo = QFileDialog.getSaveFileName(self,
                self.trUtf8("Guardar archivo"), carpeta)
        if not nombre_archivo:
            return False
        nombre_archivo = manejador_de_archivo.escribir_archivo(nombre_archivo,
                weditor.texto)
        weditor.iD = nombre_archivo
        weditor.guardado()

    def guardar_todo(self):
        for editor in self.stack.editores:
            self.guardar_archivo(editor)

    def guardar_seleccionado(self, archivo):
        for i in range(self.stack.contar):
            if self.stack.editor(i).iD == archivo:
                self.guardar_archivo(self.stack.editor(i))

    def archivos_sin_guardar(self):
        return self.stack.archivos_sin_guardar()

    def check_archivos_sin_guardar(self):
        return self.stack.check_archivos_sin_guardar()

    def busqueda_rapida(self):
        #FIXME:
        dialogo = busqueda.PopupBusqueda(self.widget_actual)
        dialogo.show()

    def deshacer(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.deshacer()

    def rehacer(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.rehacer()

    def cortar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.cortar()

    def copiar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.copiar()

    def pegar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.pegar()

    def acercar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_in()

    def seleccionar_todo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.seleccionar()

    def alejar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_out()

    def archivos_abiertos(self):
        return self.stack.archivos_abiertos()

    def propiedades_de_archivo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            dialogo = dialogo_propiedades.FileProperty(weditor, self)
            dialogo.show()

    def archivo_log(self):
        dialogo = dialogo_log.DialogoLog(self)
        dialogo.show()

    def actualizar_cursor(self, linea, columna):
        weditor = self.devolver_editor()
        lineas = weditor.lineas
        self.posicion_cursor.emit(linea + 1, columna + 1, lineas)

    def compilar_codigo_fuente(self):
        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        weditor = self.devolver_editor()
        if weditor is not None:
            self.guardar_archivo(weditor)
            output.compilar(weditor.iD)

    def ejecutar_programa(self):
        """ Ejecuta el programa objeto """

        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        output.ejecutar()

    def terminar_programa(self):
        edis = EDIS.componente("edis")
        edis.contenedor_output.terminar_programa()


principal = EditorContainer()