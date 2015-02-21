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
from src.ui.main import EDIS


class DockManager(QObject):

    def __init__(self):
        super(DockManager, self).__init__()
        # Tool buttons
        self.symbols_button = tool_button.CustomToolButton(
            self.tr("Símbolos"))
        self.navigator_button = tool_button.CustomToolButton(
            self.tr("Navegador"))
        self.explorer_button = tool_button.CustomToolButton(
            self.tr("Explorador"))

        # Conexiones
        self.connect(self.symbols_button, SIGNAL("toggled(bool)"),
                     self._symbols_visibility)
        self.connect(self.navigator_button, SIGNAL("toggled(bool)"),
                     self._navigator_visibility)
        self.connect(self.explorer_button, SIGNAL("toggled(bool)"),
                     self._explorer_visibility)

        EDIS.cargar_componente("dock", self)

    def load_dock_toolbar(self, toolbar):
        for tb in [self.symbols_button, self.navigator_button,
                   self.explorer_button]:
            toolbar.addWidget(tb)

    def load_output_widget(self, output_widget):
        self._output_widget = output_widget
        self._output_widget.hide()
        editor_container = EDIS.componente("principal")
        self.connect(output_widget, SIGNAL("goToLine(int)"),
                     editor_container.go_to_line)

    def load_symbols_widget(self, symbols_widget):
        self._symbols_widget = symbols_widget
        editor_container = EDIS.componente("principal")
        self.connect(self._symbols_widget, SIGNAL("goToLine(int)"),
                     editor_container.go_to_line)
        self.connect(self._symbols_widget, SIGNAL("visibilityChanged(bool)"),
                     lambda checked: self.symbols_button.setChecked(checked))

    def load_navigator_widget(self, navigator_widget):
        self._navigator_widget = navigator_widget
        navigator_widget.hide()
        editor_container = EDIS.componente("principal")
        self.connect(editor_container, SIGNAL("openedFile(QString)"),
                     navigator_widget.add_item)
        self.connect(editor_container, SIGNAL("closedFile(int)"),
                     navigator_widget.delete_item)
        self.connect(self._navigator_widget, SIGNAL("visibilityChanged(bool)"),
                     lambda checked: self.navigator_button.setChecked(checked))

    def load_explorer_widget(self, explorer_widget):
        self._explorer_widget = explorer_widget
        explorer_widget.hide()
        self.connect(self._explorer_widget, SIGNAL("visibilityChanged(bool)"),
                     lambda checked: self.explorer_button.setChecked(checked))

    def _symbols_visibility(self, value):
        if value:
            for widget in [self._navigator_widget, self._explorer_widget]:
                    widget.hide()
            self._symbols_widget.show()
        else:
            self._symbols_widget.hide()

    def _navigator_visibility(self, value):
        if value:
            for widget in [self._symbols_widget, self._explorer_widget]:
                widget.hide()
            self._navigator_widget.show()
        else:
            self._navigator_widget.hide()

    def _explorer_visibility(self, value):
        if value:
            for widget in [self._symbols_widget, self._navigator_widget]:
                widget.hide()
            self._explorer_widget.show()
        else:
            self._explorer_widget.hide()

    def output_visibility(self):
        if self._output_widget.isVisible():
            self._output_widget.hide()
        else:
            self._output_widget.show()

    def show_hide_all(self):
        toolbars = EDIS.componente("toolbars")
        if (self._output_widget.isVisible() or toolbars[0].isVisible() or
                toolbars[1].isVisible() or self._symbols_widget.isVisible()):
            if self._output_widget:
                self._output_widget.hide()
            if toolbars[0]:
                toolbars[0].hide()
            if toolbars[1]:
                toolbars[1].hide()
            if self._symbols_widget:
                self._symbols_widget.hide()
        else:
            if toolbars[1]:
                toolbars[1].show()
            if toolbars[0]:
                toolbars[0].show()
            if self._symbols_widget:
                self._symbols_widget.show()


dock_manager = DockManager()