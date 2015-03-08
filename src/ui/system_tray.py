# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser
from urllib import request

from PyQt4.QtGui import (
    QSystemTrayIcon,
    QMenu,
    QIcon
    )

from PyQt4.QtCore import (
    QThread,
    pyqtSignal,
    SIGNAL
    )

from src import ui
from src.helpers import logger

log = logger.edis_logger.get_logger(__name__)
INFO = log.info


class NotificacionActualizacion(QSystemTrayIcon):

    """ System Tray Icon """

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(":image/edis"))
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        exit_action = self.menu.addAction(self.tr("Salir"))
        self.thread = Thread()

        # Conexiones
        self.connect(self.thread,
                     SIGNAL("updateVersion(QString, QString, bool)"),
                     self._show_tray)
        self.connect(exit_action, SIGNAL("triggered()"), self.hide)

        self.thread.start()
        self.setToolTip(self.tr("Comprobando actualización..."))

    def _show_tray(self, version, link, found):
        """ Muestra el system tray icon """

        if found:
            self.menu.clear()
            download_action = self.menu.addAction(self.tr("Descargar!"))
            exit_action = self.menu.addAction(self.tr("Cerrar notificaciones"))

            self.connect(download_action, SIGNAL("triggered()"),
                         lambda: webbrowser.open_new(link))
            self.connect(exit_action, SIGNAL("triggered()"), self.hide)
            self.showMessage(self.tr("Nueva versión disponible!"),
                             self.tr("Existe una nueva versión de Edis!\n"
                             "versión: %s." % version),
                             QSystemTrayIcon.Information, 10000)
        else:
            self.hide()
            self.thread.terminate()


class Thread(QThread):

    """ Este hilo compara la versión local con la versión más reciente en el
    repositorio y emite la señal con los resultados """

    updateVersion = pyqtSignal('QString', 'QString', bool)

    def run(self):
        try:
            found = False
            web_version = request.urlopen(
                ui.__version_web__).read().decode('utf-8').strip()
            current_version = ui.__version__
            if current_version < web_version:
                found = True
            self.updateVersion.emit(web_version, ui.__web__, found)
        except:
            INFO("No se pudo establecer la conexión")