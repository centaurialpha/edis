# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QIcon
    )

from PyQt4.QtCore import (
    SIGNAL,
    QThread
    )
from src import recursos
from src.helpers import configuraciones
from src.ui.widgets.creador_widget import ComboSelector
from src.ui.contenedores.lateral import (
    arbol_simbolos,
    file_explorer,
    file_navigator
    )
from src.ectags.ctags import (
    CTags,
    Parser
    )


class LateralContainer(QWidget):
    icon = {
        'symbol': recursos.ICONOS['struct'],
        'navigator': recursos.ICONOS['folder-open'],
        'explorer': recursos.ICONOS['folder-open']
        }

    def __init__(self, parent):
        super(LateralContainer, self).__init__()
        self.thread_symbols = ThreadSimbolos()
        self.symbols_widget = None
        if configuraciones.SYMBOLS:
            self.symbols_widget = arbol_simbolos.ArbolDeSimbolos()

        self.file_explorer = None
        if configuraciones.FILE_EXPLORER:
            self.file_explorer = file_explorer.Explorador()

        self.file_navigator = None
        if configuraciones.FILE_NAVIGATOR:
            self.file_navigator = file_navigator.Navegador()

        self.lateral_widgets = OrderedDict([
            (self.trUtf8('Símbolos'), [QIcon(self.icon['symbol']),
                                        self.symbols_widget]),
            (self.trUtf8('Navegador'), [QIcon(self.icon['navigator']),
                                        self.file_navigator]),
            (self.trUtf8('Explorador'), [QIcon(self.icon['explorer']),
                                        self.file_explorer])
            ])

        self.load_ui()

        self.connect(self.combo_selector, SIGNAL("currentIndexChanged(int)"),
            lambda: self.change_widget(self.combo_selector.currentIndex()))

    def load_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.combo_selector = ComboSelector()
        self.combo_selector.setObjectName("combo_selector")
        self.combo_selector.setStyleSheet(
            "QComboBox::drop-down{image: url(%s); top: 0px;}"
            % recursos.ICONOS['down'])
        vbox.addWidget(self.combo_selector)

        for widget in list(self.lateral_widgets.keys()):
            self.combo_selector.addItem(
                self.lateral_widgets[widget][0], widget)

        self.stack = Stack()
        vbox.addWidget(self.stack)

        for widget in list(self.lateral_widgets.values()):
            self.stack.addWidget(widget[1])

    def change_widget(self, indice):
        if not self.isVisible():
            self.show()
        self.stack.mostrar_widget(indice)

    def actualizar_simbolos(self, archivo):
        self.thread_symbols.run(archivo)
        symbols = self.thread_symbols.parser.get_symbols()
        self.symbols_widget.actualizar_simbolos(symbols)


class ThreadSimbolos(QThread):

    def __init__(self):
        super(ThreadSimbolos, self).__init__()
        self.ctags = CTags()
        self.parser = Parser()

    def run(self, archivo):
        tag = self.ctags.start_ctags(archivo)
        tag = tag.decode()
        self.parser.parser_tag(tag)


class Stack(QStackedWidget):

    def __init__(self):
        super(Stack, self).__init__()

    def setCurrentIndex(self, indice):
        QStackedWidget.setCurrentIndex(self, indice)

    def mostrar_widget(self, indice):
        self.setCurrentIndex(indice)