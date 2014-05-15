#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QObject

from side_c import recursos


class MenuVer(QObject):

    def __init__(self, menu_ver, ide):
        super(MenuVer, self).__init__()

        accionFullScreen = menu_ver.addAction(
            self.trUtf8("Pantalla completa"))
        menu_ver.addSeparator()
        accionZoomIn = menu_ver.addAction(
            self.trUtf8("Zoom +"))
        accionZoomOut = menu_ver.addAction(
            self.trUtf8("Zoom -"))
