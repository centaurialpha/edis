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
    QStackedLayout,
    QFileDialog,
    )

from PyQt4.QtCore import (
    SIGNAL,
    QFileInfo,
    pyqtSignal
    )

from src.helpers import manejador_de_archivo
from src import recursos
from src.ui.editor import editor, editor_widget
from src.ui.edis_main import EDIS
from src.ui.widgets import busqueda
from src.ui.contenedores import selector
from src.ui.dialogos import (
    dialogo_propiedades
    )


class EditorContainer(QWidget):

    archivo_cambiado = pyqtSignal(['QString'])

    def __init__(self, edis=None):
        QWidget.__init__(self, edis)
        self.setAcceptDrops(True)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # Stacked
        self.stack = QStackedLayout()
        vbox.addLayout(self.stack)

        self.com = editor_widget.EditorWidget(self)
        self.widget_actual = self.com
        vbox.addWidget(self.com)

        EDIS.cargar_componente("principal", self)
        self.instalar_signals()

    def instalar_signals(self):
        self.connect(self.widget_actual, SIGNAL("Guardar_Editor_Actual()"),
                    self.guardar_archivo)
        self.connect(self.widget_actual.stack, SIGNAL("currentChanged(int)"),
                    self.cambiar_widget)

    def cambiar_widget(self, indice):
        """ Señal emitida cuando se cambia de editor """

        nombre_archivo = self.widget_actual.stack.widget(indice).iD
        self.archivo_cambiado.emit(nombre_archivo)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        editor_widget = self.com.agregar_editor(nombre)
        return editor_widget

    def abrir_archivo(self, nombre=""):
        if not nombre:
            carpeta = os.path.expanduser("~")
            editor_widget = self.currentWidget()
            if editor_widget and editor_widget.iD:
                carpeta = self.__ultima_carpeta_visitada(editor_widget.iD)
            archivos = QFileDialog.getOpenFileNames(self,
                            self.trUtf8("Abrir archivo"), carpeta,
                            recursos.EXTENSIONES)
        else:
            archivos = [nombre]
        for archivo in archivos:
            if not self.__archivo_abierto(archivo):
                self.widget_actual.no_esta_abierto = False
                contenido = manejador_de_archivo.leer_contenido_de_archivo(
                            archivo)
                nuevo_editor = self.agregar_editor(archivo)
                nuevo_editor.texto = contenido
                nuevo_editor.iD = archivo
                self.archivo_cambiado.emit(archivo)

        self.widget_actual.no_esta_abierto = True

    def __ultima_carpeta_visitada(self, path):
        """ Devuelve la última carpeta a la que se accedió """

        return QFileInfo(path).absolutePath()

    def __archivo_abierto(self, archivo):
        """
        Retorna True si un archivo ya esta abierto,
        False en caso contrario

        """

        editores = self.widget_actual.editores
        for editor_widget in editores:
            if editor_widget.iD == archivo:
                return True
        return False

    def agregar_widget(self, widget):
        """ Agrega @widget al stacked """

        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def eliminar_widget(self, widget):
        """ Elimina el @widget del stacked """

        self.stack.removeWidget(widget)

    def currentWidget(self):
        """ Widget actual """

        return self.widget_actual.currentWidget()

    def devolver_editor(self):
        """ Devuelve el Editor si el widget actual es una instancia de él,
        de lo contrario devuelve None. """

        widget = self.currentWidget()
        if isinstance(widget, editor.Editor):
            return widget
        return None

    def cerrar_archivo(self):
        self.widget_actual.cerrar()

    def cerrar_todo(self):
        self.widget_actual.cerrar_todo()

    def selector(self):
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

    def guardar_todo(self):
        for editor in self.widget_actual.editores:
            self.guardar_archivo(editor)

    def archivos_sin_guardar(self):
        return self.widget_actual.archivos_sin_guardar()

    def busqueda_rapida(self):
        #FIXME:
        dialogo = busqueda.PopupBusqueda(self.widget_actual,
                                        self.widget_actual.frame.combo)
        dialogo.show()

    def archivos_abiertos(self):
        return self.widget_actual.archivos_abiertos()

    def propiedades_de_archivo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            dialogo = dialogo_propiedades.FileProperty(weditor, self)
            dialogo.show()

principal = EditorContainer()