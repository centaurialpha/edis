# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtCore import (
    QObject,
    SIGNAL
    )

from src.ui.widgets import tool_button
from src.ui.main import Edis
from src.ui import thread_parse


class DockManager(QObject):

    """ Esta clase maneja los Docks """

    def __init__(self):
        super(DockManager, self).__init__()
        # Thread
        self.thread = thread_parse.Thread()
        self.connect(self.thread,
                     SIGNAL("symbols(PyQt_PyObject, PyQt_PyObject)"),
                     self._update_symbols_widget)
        # Tool buttons
        self.symbols_button = tool_button.CustomToolButton("Symbols")
        self.explorer_button = tool_button.CustomToolButton("Explorer")

        # Conexiones
        self.connect(self.symbols_button, SIGNAL("clicked(bool)"),
                     self._symbols_visibility)
        self.connect(self.explorer_button, SIGNAL("clicked(bool)"),
                     self._explorer_visibility)

        Edis.load_component("dock", self)

    def load_dock_toolbar(self, toolbar):
        """ Carga la barra de herramientas del Dock Lateral"""

        for tb in [self.symbols_button, self.explorer_button]:
            toolbar.addWidget(tb)

    def load_output_widget(self, output_widget):
        """ Carga el widget del compilador """

        self._output_widget = output_widget
        self._output_widget.hide()
        editor_container = Edis.get_component("principal")
        self.connect(output_widget, SIGNAL("goToLine(int)"),
                     editor_container.go_to_line)

    def load_symbols_widget(self, symbols_widget):
        """ Carga widget de símbolos """

        self._symbols_widget = symbols_widget
        self._symbols_widget.hide()
        editor_container = Edis.get_component("principal")
        self.connect(self._symbols_widget, SIGNAL("goToLine(int)"),
                     editor_container.go_to_line)
        self.connect(editor_container, SIGNAL("updateSymbols(QString)"),
                     lambda filename: self.thread.parse(filename))
        self.connect(editor_container.editor_widget,
                     SIGNAL("allFilesClosed()"),
                     self._symbols_widget.tree.clear)
        self.connect(self._symbols_widget, SIGNAL("visibilityChanged(bool)"),
                     lambda checked: self.symbols_button.setChecked(checked))

    def load_explorer_widget(self, explorer_widget):
        """ Carga el explorador """

        self._explorer_widget = explorer_widget
        explorer_widget.hide()
        self.connect(self._explorer_widget, SIGNAL("visibilityChanged(bool)"),
                     lambda checked: self.explorer_button.setChecked(checked))

    def _symbols_visibility(self, value):
        """ Cambia la visibilidad del árbol de símbolos """

        if value:
            self._explorer_widget.hide()
            self._symbols_widget.show()
        else:
            self._symbols_widget.hide()

    def _explorer_visibility(self, value):
        """ Cambia la visibilidad del explorador """

        if value:
            self._symbols_widget.hide()
            self._explorer_widget.show()
        else:
            self._explorer_widget.hide()

    def output_visibility(self):
        """ Cambia la visibilidad de la salida del compilador """

        if self._output_widget.isVisible():
            self._output_widget.hide()
        else:
            self._output_widget.show()

    def show_hide_all(self):
        """ Oculta todo excepto el editor y la barra de menú """

        toolbars = Edis.get_component("toolbars")
        status_bar = Edis.get_component("barra_de_estado")
        if (self._output_widget.isVisible() or toolbars[0].isVisible() or
                toolbars[1].isVisible() or self._symbols_widget.isVisible() or
                status_bar.isVisible()):
            if self._output_widget:
                self._output_widget.hide()
            if toolbars[0]:
                toolbars[0].hide()
            if toolbars[1]:
                toolbars[1].hide()
            if status_bar:
                status_bar.hide()
            if self._symbols_widget:
                self._symbols_widget.hide()
        else:
            if toolbars[1]:
                toolbars[1].show()
            if toolbars[0]:
                toolbars[0].show()
            if status_bar:
                status_bar.show()
            if self._symbols_widget:
                self._symbols_widget.show()

    def _update_symbols_widget(self, symbols, symbols_combo):
        editor_container = Edis.get_component("principal")
        symbols_combo = sorted(symbols_combo.items())
        editor_container.add_symbols_combo(symbols_combo)
        syntax_ok = True if symbols else False
        self.emit(SIGNAL("updateSyntaxCheck(bool)"), syntax_ok)
        self._symbols_widget.update_symbols(symbols)


dock_manager = DockManager()
