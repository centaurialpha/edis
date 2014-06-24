#-*- coding: utf-8 -*-

from PyQt4.QtGui import QShortcut
#from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from side_c import recursos


class MenuVer(QObject):

    def __init__(self, menu_ver, ide):
        super(MenuVer, self).__init__()

        self.ide = ide

        # Se cargan los atajos
        self.atajoFullScreen = QShortcut(
            recursos.ATAJOS['fullscreen'], self.ide)
        self.atajoModoDev = QShortcut(
            recursos.ATAJOS['modo-dev'], self.ide)
        self.atajoOcultarToolbar = QShortcut(
            recursos.ATAJOS['ocultar-toolbar'], self.ide)
        self.atajoOcultarInput = QShortcut(
            recursos.ATAJOS['ocultar-input'], self.ide)
        self.atajoOcultarMenu = QShortcut(
            recursos.ATAJOS['ocultar-menu'], self.ide)
        self.atajoZoomMas = QShortcut(
            recursos.ATAJOS['zoom-mas'], self.ide)
        self.atajoZoomMenos = QShortcut(
            recursos.ATAJOS['zoom-menos'], self.ide)

        # Conexiones
        self.connect(self.atajoFullScreen, SIGNAL("activated()"),
            self.pantalla_completa)
        self.connect(self.atajoModoDev, SIGNAL("activated()"),
            self.modo_dev)
        self.connect(self.atajoOcultarToolbar, SIGNAL("activated()"),
            self.ocultar_mostrar_toolbars)
        self.connect(self.atajoOcultarInput, SIGNAL("activated()"),
            self.visibilidad_contenedor_secundario)
        self.connect(self.atajoOcultarMenu, SIGNAL("activated()"),
            self.ocultar_mostrar_menu)
        self.connect(self.atajoZoomMas, SIGNAL("activated()"),
            self._zoom_mas)
        self.connect(self.atajoZoomMenos, SIGNAL("activated()"),
            self._zoom_menos)

        # Acciones
        self.accionFullScreen = menu_ver.addAction(
            self.trUtf8("Pantalla Completa"))
        self.accionFullScreen.setCheckable(True)
        self.accionMostrarOcultarTodo = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultar Todo"))
        menu_ver.addAction(self.accionMostrarOcultarTodo)
        self.accionMostrarOcultarTodo.setCheckable(True)
        menu_ver.addSeparator()
        self.accionMostrarOcultarToolbar = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultar Toolbars"))
        self.accionMostrarOcultarToolbar.setCheckable(True)
        self.accionMostrarOcultarEditor = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultar Editor"))
        self.accionMostrarOcultarEditor.setCheckable(True)
        self.accionMostrarOcultar_input = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultar Input"))
        self.accionMostrarOcultar_input.setCheckable(True)
        self.accionMostrarOcultar_menu = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultar Menu"))
        self.accionMostrarOcultar_menu.setCheckable(True)
        menu_ver.addSeparator()
        self.accionZoomMas = menu_ver.addAction(
            self.trUtf8("Zoom +"))
        self.accionZoomMenos = menu_ver.addAction(
            self.trUtf8("Zoom -"))

        # Conexiones a slot
        self.accionFullScreen.triggered.connect(self.pantalla_completa)
        self.accionMostrarOcultarTodo.triggered.connect(self.modo_dev)
        self.accionMostrarOcultarToolbar.triggered.connect(
            self.ocultar_mostrar_toolbars)
        self.accionMostrarOcultarEditor.triggered.connect(
            self.visibilidad_contenedor_principal)
        self.accionMostrarOcultar_input.triggered.connect(
            self.visibilidad_contenedor_secundario)
        self.accionMostrarOcultar_menu.triggered.connect(
            self.ocultar_mostrar_menu)
        self.accionZoomMas.triggered.connect(self._zoom_mas)
        self.accionZoomMenos.triggered.connect(self._zoom_menos)

        self.accionFullScreen.setChecked(False)
        self.accionMostrarOcultarTodo.setChecked(False)
        self.accionMostrarOcultarToolbar.setChecked(True)
        self.accionMostrarOcultarEditor.setChecked(True)
        self.accionMostrarOcultar_input.setChecked(False)
        self.accionMostrarOcultar_menu.setChecked(True)

    def pantalla_completa(self):
        """ Muestra en pantalla completa. """

        if self.ide.isFullScreen():
            self.ide.showMaximized()
        else:
            self.ide.showFullScreen()

    def ocultar_mostrar_toolbars(self):
        """ Muestra/oculta las toolbars """

        if self.ide.toolbar.isVisible() and self.ide.toolbar_.isVisible():
            self.ide.toolbar.hide()
            self.ide.toolbar_.hide()
        else:
            self.ide.toolbar.show()
            self.ide.toolbar_.show()

    def ocultar_mostrar_menu(self):
        """ Muestra/Oculta menuBar """

        if self.ide.menuBar().isVisible():
            self.ide.menuBar().hide()
        else:
            self.ide.menuBar().show()

    def visibilidad_contenedor_principal(self):
        self.ide.widget_Central.visibilidad_contenedor_principal()
        self.ide._menu_ver.accionMostrarOcultarEditor.setChecked(
            self.ide.widget_Central.contenedor_principal.isVisible())

    def visibilidad_contenedor_secundario(self):
        self.ide.widget_Central.mostrar_ocultar_widget_bottom()
        self.ide._menu_ver.accionMostrarOcultar_input.setChecked(
            self.ide.widget_Central.contenedor_bottom.isVisible())

    def modo_dev(self):
        """ Oculta/Muestra todo excepto el editor. """

        if self.ide.menuBar().isVisible():
            self.ide.toolbar.hide()
            self.ide.toolbar_.hide()
            self.ide.menuBar().hide()
            self.ide.contenedor_secundario.hide()
        else:
            self.ide.toolbar.show()
            self.ide.toolbar_.show()
            self.ide.menuBar().show()
        self.ide._menu_ver.accionMostrarOcultarTodo.setChecked(
            self.ide.menuBar().isVisible())
        self.ide._menu_ver.accionMostrarOcultar_input.setChecked(
            self.ide.widget_Central.contenedor_bottom.isVisible())
        self.ide._menu_ver.accionMostrarOcultarEditor.setChecked(
            self.ide.widget_Central.contenedor_principal.isVisible())
        self.ide._menu_ver.accionMostrarOcultarToolbar.setChecked(
            self.ide.toolbar.isVisible())
        self.ide._menu_ver.accionMostrarOcultarToolbar.setChecked(
            self.ide.toolbar_.isVisible())

    def _zoom_mas(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            editor.zoom_mas()

    def _zoom_menos(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            editor.zoom_menos()
