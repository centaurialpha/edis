#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c import recursos


class MenuVer(QObject):

    def __init__(self, menu_ver, ide):
        super(MenuVer, self).__init__()

        self.ide = ide

        # Acciones
        accionFullScreen = menu_ver.addAction(
            self.trUtf8("Pantalla completa"))
        accionFullScreen.setShortcut(Qt.Key_F11)
        menu_ver.addSeparator()
        self.accionMostrarOcultar_toolbars = menu_ver.addAction(
            self.trUtf8("Mostrar/Ocultara Toolbars"))
        self.accionMostrarOcultar_toolbars.setCheckable(True)
        menu_ver.addSeparator()
        accionZoomIn = menu_ver.addAction(
            self.trUtf8("Zoom +"))
        accionZoomOut = menu_ver.addAction(
            self.trUtf8("Zoom -"))

        # Conexiones
        accionFullScreen.triggered.connect(self.pantalla_completa)
        self.connect(self.accionMostrarOcultar_toolbars, SIGNAL("triggered()"),
            self.ocultar_mostrar_toolbars)

        self.accionMostrarOcultar_toolbars.setChecked(True)

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