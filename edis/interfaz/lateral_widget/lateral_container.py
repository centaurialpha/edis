# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import (
    QTabWidget,
    )

from PyQt4.QtCore import QThread

from edis.nucleo import configuraciones
from edis.interfaz.lateral_widget import (
    arbol_simbolos,
    file_explorer,
    file_navigator
    )
from edis.ectags.ctags import (
    CTags,
    Parser
    )


class LateralContainer(QTabWidget):
    """ Lateral tabs, container explorer, symbols, and browser """

    def __init__(self, parent):
        super(LateralContainer, self).__init__()
        self.setTabPosition(QTabWidget.West)
        self.thread_symbols = ThreadSimbolos()

        self.symbols_widget = None
        self.file_explorer = None
        self.file_navigator = None

        if configuraciones.SYMBOLS:
            self.add_symbols_widget()

        self.add_file_explorer()
        self.add_file_navigator()

    def add_symbols_widget(self):
        if not self.symbols_widget:
            self.symbols_widget = arbol_simbolos.ArbolDeSimbolos()
            self.addTab(self.symbols_widget, self.trUtf8("Símbolos"))

    def add_file_explorer(self):
        self.file_explorer = file_explorer.Explorador()
        self.addTab(self.file_explorer, self.trUtf8("Explorador"))

    def add_file_navigator(self):
        self.file_navigator = file_navigator.Navegador()
        self.addTab(self.file_navigator, self.trUtf8("Navegador"))

    def actualizar_simbolos(self, archivo):
        self.thread_symbols.run(archivo)
        simbolos = self.thread_symbols.parser.symbols
        self.symbols_widget.actualizar_simbolos(simbolos)


class ThreadSimbolos(QThread):

    def __init__(self):
        super(ThreadSimbolos, self).__init__()
        self.ctags = CTags()
        self.parser = Parser()

    def run(self, archivo):
        tag = self.ctags.start_ctags(archivo)
        self.parser.parser_tag(tag)