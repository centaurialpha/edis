# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import (
    QShortcut,
    QKeySequence,
    QDockWidget,
    QWidget
    )

# Módulos QtCore
from PyQt4.QtCore import Qt

from src.ui.containers.output import process
from src.ui.main import Edis


class ContenedorOutput(QDockWidget):

    def __init__(self):
        QDockWidget.__init__(self)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        barra_titulo = self.titleBarWidget()
        self._quitar_titulo(barra_titulo)

        self.nombre_archivo = None

        self.salida_ = process.EjecutarWidget()
        self.setWidget(self.salida_)

        # Conexiones
        self.atajoEscape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.atajoEscape.activated.connect(self.hide)

        Edis.load_component("output", self)

    def _quitar_titulo(self, title_bar):
        """ Quita la barra de título del DockWidget """

        widget_vacio = QWidget()
        self.setTitleBarWidget(widget_vacio)
        del title_bar

    def build(self, path):
        self.show()
        self.nombre_archivo = path
        self.salida_.run_compilation(self.nombre_archivo)

    def run(self):
        if self.nombre_archivo is None:
            return
        self.salida_.run_program(self.nombre_archivo)

    def build_and_run(self, archivo):
        self.show()
        self.nombre_archivo = archivo
        self.salida_.build_and_run(self.nombre_archivo)

    def clean(self):
        self.salida_.clean(self.nombre_archivo)

    def stop(self):
        self.salida_.kill_process()


output = ContenedorOutput()