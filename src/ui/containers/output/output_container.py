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
        title_bar = self.titleBarWidget()
        self._remove_titlebar(title_bar)

        self._filename = None

        self.salida_ = process.EjecutarWidget()
        self.setWidget(self.salida_)

        # Conexiones
        self.atajoEscape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.atajoEscape.activated.connect(self.hide)

        Edis.load_component("output", self)

    def _remove_titlebar(self, title_bar):
        """ Quita la barra de título del DockWidget """

        empty_widget = QWidget()
        self.setTitleBarWidget(empty_widget)
        del title_bar

    def build(self, path):
        self.show()
        self._filename = path
        self.salida_.run_compilation(self._filename)

    def run(self):
        if self._filename is None:
            return
        self.salida_.run_program(self._filename)

    def build_and_run(self, filename):
        self.show()
        self._filename = filename
        self.salida_.build_and_run(self._filename)

    def clean(self):
        self.salida_.clean(self._filename)

    def stop(self):
        self.salida_.kill_process()


output = ContenedorOutput()
