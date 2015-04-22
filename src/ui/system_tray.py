# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
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
from src.core import logger

log = logger.edis_logger.get_logger(__name__)
INFO = log.info


class NotificacionActualizacion(QSystemTrayIcon):

    """ System Tray Icon """

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(":image/edis"))
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        exit_action = self.menu.addAction(self.tr("Close"))
        self.thread = Thread()

        # Conexiones
        self.connect(self.thread,
                     SIGNAL("updateVersion(QString, QString, bool)"),
                     self._show_tray)
        self.connect(exit_action, SIGNAL("triggered()"), self.hide)

        self.setToolTip(self.tr("Checking updates..."))
        self.thread.start()

    def _show_tray(self, version, link, found):
        """ Muestra el system tray icon """

        if found:
            self.menu.clear()
            self.setToolTip("")
            download_action = self.menu.addAction(self.tr("Download!"))
            exit_action = self.menu.addAction(self.tr("Close notifications"))

            self.connect(download_action, SIGNAL("triggered()"),
                         lambda: webbrowser.open_new(link))
            self.connect(exit_action, SIGNAL("triggered()"), self.hide)
            self.showMessage(self.tr("New version available!"),
                             self.tr("New version of Edis available!\n"
                             "version: {0}.").format(version),
                             QSystemTrayIcon.Information, 10000)
        else:
            self.hide()


class Thread(QThread):

    """ Este hilo compara la versión local con la versión más reciente en el
    repositorio y emite la señal con los resultados """

    updateVersion = pyqtSignal('QString', 'QString', bool)

    def run(self):
        try:
            found = False
            web_version = request.urlopen(
                ui.__web_version__).read().decode('utf-8').strip()
            current_version = ui.__version__
            if current_version < web_version:
                found = True
        except:
            web_version = ''
            INFO("No se pudo establecer la conexión")
        self.updateVersion.emit(web_version, ui.__web__, found)
