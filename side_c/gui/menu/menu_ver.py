#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt

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
        accionZoomIn = menu_ver.addAction(
            self.trUtf8("Zoom +"))
        accionZoomOut = menu_ver.addAction(
            self.trUtf8("Zoom -"))

        # Conexiones
        accionFullScreen.triggered.connect(self.pantalla_completa)

    def pantalla_completa(self):
        """ Muestra en pantalla completa. """

        if self.ide.isFullScreen():
            self.ide.showMaximized()
        else:
            self.ide.showFullScreen()