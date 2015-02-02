# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser

from PyQt4.QtGui import (
    QSystemTrayIcon,
    QMenu,
    QAction,
    QIcon
    )

from PyQt4.QtCore import (
    QThread,
    pyqtSignal
    )

#from src import ui
from src import paths

FASES = {
    'rc': 2,
    'beta': 1,
    'alpha': 0
    }


class NotificacionActualizacion(QSystemTrayIcon):

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(paths.ICONOS['new']))
        self.hilo = Thread()
        self.hilo.start()
        self.hilo.version.connect(self._mostrar_mensaje)

    def _mostrar_mensaje(self, version, link):
        menu = QMenu()
        accion_descarga = QAction("Descargar", self)
        accion_descarga.triggered.connect(lambda: webbrowser.open_new(link))
        accion_salir = QAction("Salir", self)
        accion_salir.triggered.connect(self.hide)
        menu.addAction(accion_descarga)
        menu.addSeparator()
        menu.addAction(accion_salir)
        self.setContextMenu(menu)
        self.showMessage(self.tr("Actualización"),
                        self.tr("Existe una nueva versión de EDIS!"))


class Thread(QThread):

    version = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def run(self):
        pass