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
from PyQt4.QtCore import (
    Qt,
    SIGNAL
    )

from src.ui.containers.output import process
from src.ui.main import Edis


class OutputContainer(QDockWidget):

    def __init__(self):
        QDockWidget.__init__(self)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        title_bar = self.titleBarWidget()
        self._remove_titlebar(title_bar)

        #self._filename = None
        self._sources = None

        self.salida_ = process.EjecutarWidget()
        self.setWidget(self.salida_)

        # Conexiones
        key_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(key_escape, SIGNAL("activated()"), self.hide)

        Edis.load_component("output", self)

    def _remove_titlebar(self, title_bar):
        """ Quita la barra de título del DockWidget """

        empty_widget = QWidget()
        self.setTitleBarWidget(empty_widget)
        del title_bar

    def build(self, sources):
        self.show()
        self._sources = sources
        self.salida_.run_compilation(self._sources)
        self.setFocus()

    def run(self):
        if self._sources is None:
            return
        self.salida_.run_program(self._sources)

    def build_and_run(self, sources):
        self.show()
        self._sources = sources
        self.salida_.build_and_run(self._sources)

    def clean(self):
        self.salida_.clean(self._filename)

    def stop(self):
        self.salida_.kill_process()


output = OutputContainer()
