# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
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
from src import ui
from src.ui import system_tray
from src.helpers import (
    configuracion,
    #dependencias
    )
#from src.ui.widgets import tool_button
from src.helpers.configuracion import ESettings
from src.ui.dialogos import (
    dialogo_guardar_archivos,
    #dialogo_dependencias,
    acerca_de
    )


class EDIS(QMainWindow):
    """
    Esta clase es conocedora de todas las demás.

    """

    # Cada instancia de una clase  se guarda en éste diccionario
    __COMPONENTES = {}
    __LATERAL = {}  # Widgets laterales
    __MENUBAR = {}  # Nombre de los menus
    __ACCIONES = {}

    def __init__(self):
        QMainWindow.__init__(self)
        # Esto para tener widgets laterales en full height,
        # existe otra forma?
        window = QMainWindow(self)

        self.setWindowTitle(ui.__nombre__)
        self.setMinimumSize(750, 500)
        # Se cargan las dimensiones de la ventana
        d = ESettings.get('ventana/dimensiones')
        if d:
            self.resize(d)
        else:
            self.showMaximized()
        pos = ESettings.get('ventana/posicion')
        if pos != 0:
            self.move(pos)
        # Secciones del menubar
        EDIS.menu_bar(0, self.trUtf8("&Archivo"))
        EDIS.menu_bar(1, self.trUtf8("&Editar"))
        EDIS.menu_bar(2, self.trUtf8("&Ver"))
        EDIS.menu_bar(3, self.trUtf8("&Buscar"))
        EDIS.menu_bar(4, self.trUtf8("E&jecución"))
        EDIS.menu_bar(5, self.trUtf8("A&cerca de"))
        # Toolbar
        self.toolbar = QToolBar(self)
        toggle_action = self.toolbar.toggleViewAction()
        toggle_action.setText(self.tr("Toolbar"))
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.dock_toolbar = QToolBar(self)
        toggle_action = self.dock_toolbar.toggleViewAction()
        toggle_action.setText(self.tr("Dock toolbar"))
        self.dock_toolbar.setObjectName("dock_toolbar")
        #self.tb_simbolos = tool_button.CustomToolButton("Símbolos", self)
        #self.tb_navegador = tool_button.CustomToolButton("Navegador", self)
        #self.tb_explorador = tool_button.CustomToolButton("Explorador", self)
        self.dock_toolbar.setMovable(False)
        #self.dock_toolbar.addWidget(self.tb_simbolos)
        #self.dock_toolbar.addWidget(self.tb_navegador)
        #self.dock_toolbar.addWidget(self.tb_explorador)
        self.addToolBar(Qt.LeftToolBarArea, self.dock_toolbar)
        # Animated property
        self.setDockOptions(QMainWindow.AnimatedDocks)
        # Menú
        menu_bar = self.menuBar()
        self.setup_menu(menu_bar)
        # Barra de estado
        self.barra_de_estado = EDIS.componente("barra_de_estado")
        self.setStatusBar(self.barra_de_estado)
        # Widget central
        central = self.cargar_central(window)
        window.setCentralWidget(central)
        window.setWindowFlags(Qt.Widget)
        self.setCentralWidget(window)

        EDIS.cargar_componente("edis", self)

        #self.tb_simbolos.toggled.connect(self.toggled_simbolos)
        #self.tb_navegador.toggled.connect(self.toggled_navegador)
        #self.tb_explorador.toggled.connect(self.toggled_explorador)

        # Comprobar nueva versión
        self.noti = system_tray.NotificacionActualizacion()
        self.noti.show()

    @classmethod
    def cargar_componente(cls, nombre, instancia):
        """ Se guarda el nombre y la instancia de una clase """

        cls.__COMPONENTES[nombre] = instancia

    @classmethod
    def componente(cls, nombre):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTES.get(nombre, None)

    @classmethod
    def cargar_lateral(cls, nombre, instancia):
        cls.__LATERAL[nombre] = instancia

    @classmethod
    def lateral(cls, nombre):
        return cls.__LATERAL.get(nombre, None)

    @classmethod
    def menu_bar(cls, clave, nombre):
        """ Se guarda el nombre de cada menú """

        cls.__MENUBAR[clave] = nombre

    #@classmethod
    #def get_menu(cls, clave):
        #""" Devuelve un diccionario con los menu """

        #return cls.__MENUBAR.get(clave, None)

    #@classmethod
    #def accion(cls, nombre):
        #return cls.__ACCIONES.get(nombre, None)

    def setup_menu(self, menu_bar):
        from src.ui import actions
        from src import recursos

        menu_items = {}
        editor_container = EDIS.componente("principal")
        shortcuts = recursos.SHORTCUTS
        toolbar_items = configuracion.TOOLBAR_ITEMS
        for i, m in enumerate(list(EDIS.__MENUBAR.values())):
            menu = menu_bar.addMenu(m)
            menu_items[i] = menu
        for i, _actions in enumerate(actions.ACTIONS):
            for action in _actions:
                obj = editor_container
                menu_name = menu_items[i]
                name = action.get('name', None)
                connection = action.get('connection', None)
                shortcut = action.get('shortcut', None)
                separator = action.get('separator', False)
                qaction = menu_name.addAction(name)
                #FIXME: No depender de shortcut
                icon = QIcon(":image/%s" % shortcut)
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
                #FIXME: agregar separador
                if shortcut in toolbar_items:
                    self.toolbar.addAction(qaction)

    def cargar_central(self, window):
        principal = EDIS.componente("principal")
        dock = EDIS.componente("dock")  # lint:ok
        #start_page = False
        if ESettings.get('general/inicio'):
            principal.add_start_page()
            #start_page = True
        #self.simbolos = EDIS.lateral("simbolos")
        #if start_page:
            #self.simbolos.hide()
        #self.navegador = EDIS.lateral("navegador")
        #self.navegador.hide()
        #self.explorador = EDIS.lateral("explorador")
        #self.explorador.hide()
        #self.output = EDIS.componente("output")
        #window.addDockWidget(Qt.BottomDockWidgetArea, self.output)
        #self.output.hide()
        #for widget in [self.navegador, self.explorador, self.simbolos]:
            #self.addDockWidget(Qt.LeftDockWidgetArea, widget)

        #principal.archivo_cambiado['QString'].connect(self.__actualizar_estado)
        self.connect(principal, SIGNAL("cursorPosition(int, int, int)"),
                     self._update_cursor)
        #principal.actualizarSimbolos['QString'].connect(
            #principal.update_symbols)
        #principal.archivo_cambiado.connect(principal.update_symbols)
        #self.simbolos.irALinea[int].connect(principal.ir_a_linea)
        #self.output.salida_.output.ir_a_linea[int].connect(
            #principal.ir_a_linea)
        self.connect(principal, SIGNAL("fileChanged(QString)"),
                     self._change_title)
        self.connect(principal.stack, SIGNAL("allClosed()"), self._all_closed)
        principal.stack.todo_cerrado.connect(principal.add_start_page)
        #principal.archivo_abierto['QString'].connect(self.navegador.agregar)
        #principal.archivo_cerrado[int].connect(self.navegador.eliminar)

        return principal

    def _update_cursor(self, line, row, lines):
        self.barra_de_estado.cursor_widget.show()
        self.barra_de_estado.cursor_widget.actualizar_cursor(line, row, lines)

    def _update_status(self, archivo):
        self.barra_de_estado.update_status(archivo)

    def _all_closed(self):
        self.setWindowTitle(ui.__nombre__)
        self.barra_de_estado.cursor_widget.hide()
        self._update_status("")

    def _change_title(self, titulo):
        """ Cambia el título de la ventana (nombre_archivo - EDIS) """

        titulo = os.path.basename(titulo)
        self.setWindowTitle(titulo + ' - ' + ui.__nombre__)

    def report_bug(self):
        webbrowser.open_new(ui.__reportar_bug__)

    def show_hide_toolbars(self):
        for toolbar in [self.toolbar, self.dock_toolbar]:
            if toolbar.isVisible():
                toolbar.hide()
            else:
                toolbar.show()

    def show_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cargar_archivos(self, archivos, recents_files):
        """ Carga archivos al editor desde la última sesión y actualiza el menú
        de archivos recientes.
        """

        if archivos:
            self.simbolos.show()
            principal = EDIS.componente("principal")
            for archivo in archivos:
                principal.abrir_archivo(archivo[0], archivo[1])
        #FIXME: Se está haciendo lo mismo en EditorContainer
        menu_recents_files = EDIS.accion("Abrir reciente")
        principal = EDIS.componente("principal")
        self.connect(menu_recents_files, SIGNAL("triggered(QAction*)"),
                     principal._abrir_reciente)
        for recent_file in recents_files:
            menu_recents_files.addAction(recent_file)

    def about_qt(self):
        QMessageBox.aboutQt(self)

    def about_edis(self):
        dialogo = acerca_de.AcercaDe(self)
        dialogo.exec_()

    def closeEvent(self, e):
        """
        Éste médoto es llamado automáticamente por Qt cuando se
        cierra la aplicación

        """

        principal = EDIS.componente("principal")
        if principal.check_archivos_sin_guardar() and \
                ESettings.get('general/confirmarSalida'):

            archivos_sin_guardar = principal.archivos_sin_guardar()
            dialogo = dialogo_guardar_archivos.Dialogo(
                archivos_sin_guardar, principal)
            dialogo.exec_()
            if dialogo.ignorado():
                e.ignore()
        if ESettings.get('ventana/guardarDimensiones'):
            ESettings.set('ventana/dimensiones', self.size())
            ESettings.set('ventana/posicion', self.pos())
        #ESettings.set('general/archivos', principal.archivos_abiertos())
        #ESettings.set('general/recientes', principal.get_recents_files())

    def show_settings(self):
        from src.ui.dialogos.preferencias import preferencias
        dialogo = preferencias.Preferencias(self)
        dialogo.show()
