# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDockWidget,
    QTabWidget
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.ui.main import Edis
from src.tools.ctags import ctags
from src.core import settings


class TabContainer(QDockWidget):

    def __init__(self):
        super(TabContainer, self).__init__()
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
        # Oculto cuando se inicia
        self.hide()

    def _load_context_menu(self, point):
        pass
        #menu = QMenu()
        #position_action = menu.addAction(self.tr("Change position"))

        #self.connect(position_action, SIGNAL("triggered()"),
                     #self._change_dock_position)

        #menu.exec_(self.mapToGlobal(point))

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
        self._change_border_tab_position(dock_area)

    def _change_border_tab_position(self, area):
        current_theme = settings.get_setting("window/style-sheet")
        if current_theme != 'Edark':
            return
        position = "right" if area == 1 else "left"
        border = "{border-%s: 3px solid #666}" % position
        self.tabs.setStyleSheet("QTabBar::tab:selected %s" % border)

    def load_symbols_widget(self, widget):
        if self._symbols_widget is None:
            self._symbols_widget = Edis.get_lateral("symbols")
            self.tabs.addTab(self._symbols_widget, self.tr("Símbolos"))

            # Conexiones
            editor_container = Edis.get_component("principal")
            self.connect(self._symbols_widget, SIGNAL("goToLine(int)"),
                         editor_container.go_to_line)
            self.connect(editor_container, SIGNAL("updateSymbols(QString)"),
                         self._update_symbols_widget)
                         #lambda filename: self.thread.parse(filename))
            self.connect(editor_container.editor_widget,
                         SIGNAL("allFilesClosed()"),
                         self._symbols_widget.clear)

    def load_explorer_widget(self, widget):
        if self._explorer is None:
            self._explorer = Edis.get_lateral("explorer")
            self.tabs.addTab(self._explorer, self.tr("Explorador"))

    def load_project_widget(self, widget):
        self._tree_project = Edis.get_lateral("tree_projects")
        self.tabs.addTab(self._tree_project, self.tr("Proyectos"))

        editor_container = Edis.get_component("principal")
        self.connect(editor_container, SIGNAL("projectOpened(PyQt_PyObject)"),
                     self._open_project)
        self.connect(editor_container, SIGNAL("folderOpened(PyQt_PyObject)"),
                     self._open_directory)

    def _update_symbols_widget(self, filename):
        symbols, symbols_combo = ctags.get_symbols(filename)
        editor_container = Edis.get_component("principal")
        symbols_combo = sorted(symbols_combo.items())
        editor_container.add_symbols_combo(symbols_combo)
        self._symbols_widget.update_symbols(symbols)

    def _update_tree_project(self, data):
        self._tree_project.load_project(data)

    def _open_project(self, structure):
        self._tree_project.open_project(structure)
        self.setVisible(True)
        self.tabs.setCurrentWidget(self._tree_project)

    def _open_directory(self, structure):
        self._tree_project.open_directory(structure)


tab_container = TabContainer()