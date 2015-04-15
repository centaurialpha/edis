# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import os
import webbrowser

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow,
    QIcon,
    QToolBar,
    QMessageBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    SIGNAL,
    Qt,
    QSize,
    )

# Módulos EDIS
from src import recursos
from src import ui
from src.ui import system_tray
from src.core import settings
from src.ui.dialogs import (
    unsaved_files,
    about
    )

TOOLBAR_ITEMS = ["new", "open", "save", "separator", "undo", "redo",
                 "separator", "copy", "cut", "paste", "separator", "indent",
                 "unindent", "separator", "build", "run", "stop"]


class Edis(QMainWindow):
    """
    Clase principal:
        Esta clase es la encargada de instalar todos los servicios del IDE,
        las instancias de los componentes que cumplen funciones críticas están
        disponibles desde los atributos de clase.


    """

    __COMPONENTS = {}
    __LATERAL = {}

    def __init__(self):
        QMainWindow.__init__(self)
        # Esto para tener widgets laterales en full height,
        window = QMainWindow(self)
        self.setWindowTitle('{' + ui.__edis__ + '}')
        self.setMinimumSize(750, 500)
        # Se cargan las dimensiones de la ventana
        if settings.get_setting('window/show-maximized'):
            self.setWindowState(Qt.WindowMaximized)
        else:
            size = settings.get_setting('window/size')
            position = settings.get_setting('window/position')
            self.resize(size)
            self.move(position)
        # Toolbars
        self.toolbar = QToolBar(self)
        self.toolbar.setObjectName("toolbar")
        toggle_action = self.toolbar.toggleViewAction()
        toggle_action.setText(self.tr("Toolbar"))
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        Edis.load_component("toolbar", self.toolbar)
        # Animated property
        self.setDockOptions(QMainWindow.AnimatedDocks)
        # Menú
        menu_bar = self.menuBar()
        self.setup_menu(menu_bar)
        # Barra de estado
        self.status_bar = Edis.get_component("status_bar")
        self.setStatusBar(self.status_bar)
        # Widget central
        central = self._load_ui(window)
        window.setCentralWidget(central)
        window.setWindowFlags(Qt.Widget)
        self.setCentralWidget(window)

        Edis.load_component("edis", self)
        # Comprobar nueva versión
        if settings.get_setting('general/check-updates'):
            self.noti = system_tray.NotificacionActualizacion()
            self.noti.show()

    @classmethod
    def load_component(cls, name, instance):
        """ Carga la instancia de un componente """

        cls.__COMPONENTS[name] = instance

    @classmethod
    def get_component(cls, name):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTS.get(name, None)

    @classmethod
    def load_lateral(cls, name, instance):
        """ Carga un componente lateral """

        cls.__LATERAL[name] = instance

    @classmethod
    def get_lateral(cls, name):
        """ Devuelve la instancia de un componente lateral """

        return cls.__LATERAL.get(name, None)

    def setup_menu(self, menu_bar):
        """ Instala la barra de menú (QMenuBar), acciones, shortcuts, toolbars
        y conexiones de cada QAction.
        """

        from src.ui import actions

        menubar_items = [
            self.tr("&File"),
            self.tr("&Edit"),
            self.tr("&View"),
            self.tr("&Search"),
            self.tr("&Build"),
            self.tr("&Tools"),
            self.tr("&Help")
            ]
        menu_items = {}
        toolbar_actions = {}
        editor_container = Edis.get_component("principal")
        shortcuts = recursos.SHORTCUTS
        toolbar_items = TOOLBAR_ITEMS
        for i, m in enumerate(menubar_items):
            menu = menu_bar.addMenu(m)
            menu_items[i] = menu
        for i, _actions in enumerate(actions.ACTIONS):
            for action in _actions:
                obj = editor_container
                menu_name = menu_items[i]
                name = action.get('name', None)
                connection = action.get('connection', None)
                shortcut = action.get('shortcut', None)
                icon_action = action.get('icon', None)
                if icon_action is not None:
                    icon = QIcon(":image/%s" % icon_action)
                else:
                    # FIXME: No depender de shortcut
                    icon = QIcon(":image/%s" % shortcut)
                separator = action.get('separator', False)
                subm = action.get('menu', False)
                if subm:
                    # Archivos recientes
                    submenu = menu_name.addMenu(name)
                    Edis.load_component("menu_recent_file", submenu)
                    continue
                qaction = menu_name.addAction(name)
                qaction.setIcon(icon)
                if shortcut is not None:
                    qaction.setShortcut(shortcuts[shortcut])
                if connection.startswith('edis'):
                    obj = self
                    connection = connection.split('.')[-1]
                slot = getattr(obj, connection, None)
                if hasattr(slot, "__call__"):
                    self.connect(qaction, SIGNAL("triggered()"), slot)
                if separator:
                    menu_name.addSeparator()
                if shortcut in toolbar_items:
                    toolbar_actions[shortcut] = qaction
        # Load toolbar
        for item in toolbar_items:
            action = toolbar_actions.get(item, None)
            if action is None:
                self.toolbar.addSeparator()
            else:
                self.toolbar.addAction(action)

    def _load_ui(self, window):
        """ Carga el componente principal (Editor Container), componentes
        laterales y la salida del compilador.
        """

        editor_container = Edis.get_component("principal")
        # Lateral
        tab_container = Edis.get_component("tab_container")
        lateral_widgets = ["symbols", "project", "explorer"]
        for widget in lateral_widgets:
            method = getattr(tab_container, "load_%s_widget" % widget)
            obj = Edis.get_lateral(widget)
            method(obj)
        self.addDockWidget(Qt.LeftDockWidgetArea, tab_container)
        output_widget = Edis.get_component("output")
        output_widget.hide()
        window.addDockWidget(Qt.BottomDockWidgetArea, output_widget)
        if settings.get_setting('general/show-start-page'):
            editor_container.add_start_page()

        # Conexiones
        self.connect(editor_container, SIGNAL("fileChanged(QString)"),
                     self._update_status)
        self.connect(editor_container, SIGNAL("fileChanged(QString)"),
                     self._change_title)
        self.connect(editor_container.editor_widget,
                     SIGNAL("allFilesClosed()"),
                     self._all_closed)
        self.connect(output_widget, SIGNAL("goToLine(int)"),
                     editor_container.go_to_line)

        return editor_container

    def _update_status(self, archivo):
        """ Actualiza el path del archivo en la barra de estado """

        self.status_bar.update_status(archivo)

    def _all_closed(self):
        """ Limpia la barra de estado y el título de la ventana """

        self.setWindowTitle('{' + ui.__edis__ + '}')
        self._update_status("")

    def _change_title(self, title):
        """ Cambia el título de la ventana (filename - {EDIS}) """

        title = os.path.basename(title)
        self.setWindowTitle(title + ' - ' + '{' + ui.__edis__ + '}')

    def report_bug(self):
        """ Se abre la url para reportar un bug """

        webbrowser.open_new(ui.__bug_link__)

    def show_hide_toolbar(self):
        """ Cambia la visibilidad de la barra de herramientas """

        if self.toolbar.isVisible():
            self.toolbar.hide()
        else:
            self.toolbar.show()

    def show_hide_lateral(self):
        """ Cambia la visibilidad del dock lateral """

        lateral_widget = Edis.get_component("tab_container")
        if not lateral_widget.isVisible():
            lateral_widget.show()
        else:
            lateral_widget.hide()

    def show_hide_all(self):
        """ Oculta todo excepto la barra de menú y el editor """

        toolbar = Edis.get_component("toolbar")
        status_bar = Edis.get_component("status_bar")
        output = Edis.get_component("output")
        lateral = Edis.get_component("tab_container")
        if (output.isVisible() or toolbar.isVisible() or
           status_bar.isVisible() or lateral.isVisible()):
            if output:
                output.hide()
            if toolbar:
                toolbar.hide()
            if status_bar:
                status_bar.hide()
            if lateral:
                lateral.hide()
        else:
            if toolbar:
                toolbar.show()
            if output:
                output.show()
            if status_bar:
                status_bar.show()
            if lateral:
                lateral.show()

    def show_full_screen(self):
        """ Cambia a modo FullScreen """

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_hide_output(self):
        """ Cambia la visibilidad de la salida del compilador """

        output = Edis.get_component("output")
        if output.isVisible():
            output.hide()
        else:
            output.show()

    def load_files_and_projects(self, files, recents_files, projects):
        """ Carga archivos al editor desde la última sesión y actualiza el menú
        de archivos recientes.
        """

        editor_container = Edis.get_component("principal")
        for _file in files:
            editor_container.open_file(_file)
        editor_container.update_recents_files(recents_files)
        for project in projects:
            editor_container.open_project(project)

    def about_qt(self):
        """ Muestra el díalogo acerca de Qt """

        QMessageBox.aboutQt(self)

    def about_edis(self):
        dialog = about.AcercaDe(self)
        dialog.exec_()

    def closeEvent(self, event):
        """
        Éste médoto es llamado automáticamente por Qt cuando se
        cierra la aplicación, guarda algunas configuraciones como posición y
        tamaño de la ventana, archivos, etc.

        """

        editor_container = Edis.get_component("principal")
        if editor_container.check_files_not_saved() and \
                settings.get_setting('general/confirm-exit'):
            files_not_saved = editor_container.files_not_saved()
            dialog = unsaved_files.DialogSaveFiles(
                files_not_saved, editor_container, self)
            dialog.exec_()
            if dialog.ignorado():
                event.ignore()
        if settings.get_setting('window/store-size'):
            if self.isMaximized():
                settings.set_setting('window/show-maximized', True)
            else:
                settings.set_setting('window/show-maximized', False)
                settings.set_setting('window/size', self.size())
                settings.set_setting('window/position', self.pos())
        opened_files = editor_container.opened_files()
        settings.set_setting('general/files', opened_files)
        settings.set_setting('general/recents-files',
                             editor_container.get_recents_files())
        projects = editor_container.get_open_projects()
        settings.set_setting('general/projects', projects)