# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
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

    def _symbols_visibility(self, value):
        pass

    def _navigator_visibility(self, value):
        pass

    def _explorer_visibility(self, value):
        pass


dock_manager = DockManager()