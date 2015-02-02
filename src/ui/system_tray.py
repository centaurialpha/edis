# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser
from urllib import request

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

from src import ui
from src import paths
from src.helpers import logger

log = logger.edis_logger.get_logger(__name__)


class NotificacionActualizacion(QSystemTrayIcon):

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(paths.ICONOS['icon']))
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
        self.showMessage(self.tr("Nueva versión disponible!"),
                        self.tr("Existe una nueva versión de EDIS!\n"
                        "versión: %s." % version),
                        QSystemTrayIcon.Information, 10000)


class Thread(QThread):

    version = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def run(self):
        try:
            version_web = request.urlopen(
                ui.__version_web__).read().decode('utf-8')
            version_actual, fase_actual = ui.__version__.split('-')
            version_web, fase = version_web.split('-')
            if float(version_actual) < float(version_web):
                self.version.emit(version_web, ui.__web__)
            elif fase_actual != fase:
                self.version.emit(version_web + '-' + fase, ui.__web__)
        except:
            log.info("No se pudo establecer la conexión")