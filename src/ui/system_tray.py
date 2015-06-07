# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser
import json
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

log = logger.get_logger(__name__)
INFO = log.info
DEBUG = log.debug


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

        self.setToolTip(self.tr("Buscando actualizaciones..."))
        self.thread.start()

    def _show_tray(self, version, link, found):
        """ Muestra el system tray icon """

        if found:
            self.menu.clear()
            self.setToolTip("")
            download_action = self.menu.addAction(self.tr("Descargar!"))
            exit_action = self.menu.addAction(self.tr("Cerrar notificación"))

            self.connect(download_action, SIGNAL("triggered()"),
                         lambda: webbrowser.open_new(link))
            self.connect(exit_action, SIGNAL("triggered()"), self.hide)
            self.showMessage(self.tr("Nueva versión disponible!"),
                             self.tr("Está disponible una nueva versión de"
                                     " Edis\n"
                             "versión: {0}.").format(version),
                             QSystemTrayIcon.Information, 10000)
        else:
            self.hide()


class Thread(QThread):

    """ Este hilo compara la versión local con la versión más reciente en el
    repositorio y emite la señal con los resultados """

    updateVersion = pyqtSignal('QString', 'QString', bool)

    def run(self):
        DEBUG("Searching updates...")
        found = False
        try:
            response = request.urlopen(ui.__web_version__)
            data = json.loads(response.read().decode('utf8'))
            web_version, link = data['version'], data['link']
            current_version = ui.__version__
            if current_version < web_version:
                found = True
        except:
            web_version, link = '', ''
            INFO("No se pudo establecer la conexión")
        DEBUG("Última versión disponible: {0}".format(web_version))
        self.updateVersion.emit(web_version, link, found)