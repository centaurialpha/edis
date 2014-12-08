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
    QFileDialog
    )

from src.helpers import manejador_de_archivo
from src import recursos
from src.ui.editor import editor


class EditorContainer(QWidget):

    def __init__(self, edis):
        QWidget.__init__(self, edis)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        #self.combo = combo_widget.ComboWidget(self)
        #vbox.addWidget(self.combo)

        self.stack = QStackedLayout()
        vbox.addLayout(self.stack)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        editor_widget = editor.crear_editor(nombre_archivo=nombre)
        self.stack.addWidget(editor_widget)
        return editor_widget

    def abrir_archivo(self, nombre=""):
        #FIXME: Comprobar si el archivo ya está abierto
        if not nombre:
            carpeta = os.path.expanduser("~")
            #FIXME: Abrir lista de archivos
            archivo = QFileDialog.getOpenFileName(self,
                            self.trUtf8("Abrir archivo"), carpeta,
                            recursos.EXTENSIONES)
        contenido = manejador_de_archivo.leer_contenido_de_archivo(archivo)
        nuevo_editor = self.agregar_editor(archivo)
        nuevo_editor.texto = contenido

    def currentWidget(self):
        """ Widget actual """

        return self.stack.currentWidget()

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