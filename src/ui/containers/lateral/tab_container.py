# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDockWidget,
    QTabWidget,
    QMenu
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.ui.main import Edis
from src.ui import thread_parse


class TabContainer(QDockWidget):

    def __init__(self):
        super(TabContainer, self).__init__()
        # Thread
        self.thread = thread_parse.Thread()
        self.connect(self.thread,
                     SIGNAL("symbols(PyQt_PyObject, PyQt_PyObject)"),
                     self._update_symbols_widget)
        # Areas
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.setWidget(self.tabs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Widgets
        self._symbols_widget = None
        self._explorer = None

        Edis.load_component("tab_container", self)

        self.connect(self, SIGNAL("dockLocationChanged(Qt::DockWidgetArea)"),
                     self._change_tab_position)
        self.connect(self,
                     SIGNAL("customContextMenuRequested(const QPoint)"),
                     self._load_context_menu)

    def _load_context_menu(self, point):
        menu = QMenu()
        position_action = menu.addAction(self.tr("Change position"))

        self.connect(position_action, SIGNAL("triggered()"),
                     self._change_dock_position)

        menu.exec_(self.mapToGlobal(point))

    def _change_dock_position(self):
        edis = Edis.get_component("edis")
        current_area = edis.dockWidgetArea(self)
        if current_area == Qt.LeftDockWidgetArea:
            edis.addDockWidget(Qt.RightDockWidgetArea, self)
        else:
            edis.addDockWidget(Qt.LeftDockWidgetArea, self)

    def _change_tab_position(self, dock_area):
        """ Cambia la posición de las pestañas """

        if dock_area == Qt.LeftDockWidgetArea:
            self.tabs.setTabPosition(QTabWidget.West)
        else:
            self.tabs.setTabPosition(QTabWidget.East)

    def load_symbols_widget(self, widget):
        if self._symbols_widget is None:
            self._symbols_widget = Edis.get_lateral("symbols")
            self.tabs.addTab(self._symbols_widget, self.tr("Symbols"))

            # Conexiones
            editor_container = Edis.get_component("principal")
            self.connect(self._symbols_widget, SIGNAL("goToLine(int)"),
                         editor_container.go_to_line)
            self.connect(editor_container, SIGNAL("updateSymbols(QString)"),
                         lambda filename: self.thread.parse(filename))
            self.connect(editor_container.editor_widget,
                         SIGNAL("allFilesClosed()"),
                         self._symbols_widget.clear)

    def load_explorer_widget(self, widget):
        if self._explorer is None:
            self._explorer = Edis.get_lateral("explorer")
            self.tabs.addTab(self._explorer, self.tr("Explorer"))

    def _update_symbols_widget(self, symbols, symbols_combo):
        editor_container = Edis.get_component("principal")
        symbols_combo = sorted(symbols_combo.items())
        editor_container.add_symbols_combo(symbols_combo)
        syntax_ok = True if symbols else False
        self.emit(SIGNAL("updateSyntaxCheck(bool)"), syntax_ok)
        self._symbols_widget.update_symbols(symbols)


tab_container = TabContainer()