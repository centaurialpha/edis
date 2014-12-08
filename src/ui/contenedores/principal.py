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
    QStackedWidget,
    QFileDialog
    )

from PyQt4.QtCore import *

from src.helpers import manejador_de_archivo
from src import recursos
from src.ui.editor import editor, editor_widget
from src.ui.edis_main import EDIS


class EditorContainer(QWidget):

    def __init__(self, edis=None):
        QWidget.__init__(self, edis)
        self.setAcceptDrops(True)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # Stacked
        self.stack = QStackedWidget()
        vbox.addWidget(self.stack)

        self.com = editor_widget.EditorWidget(self)
        self.widget_actual = self.com
        vbox.addWidget(self.com)

        EDIS.cargar_componente("principal", self)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        editor_widget = self.com.agregar_editor(nombre)
        return editor_widget

    def abrir_archivo(self, nombre=""):
        #FIXME: Comprobar si el archivo ya está abierto
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

    def guardar_archivo(self):
        pass

    def guardar_archivo_como(self):
        pass


principal = EditorContainer()