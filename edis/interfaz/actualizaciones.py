# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

import json
import urllib
import webbrowser
from distutils import version

from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QThread

from edis import interfaz
from edis import recursos


class Actualizacion(QSystemTrayIcon):

    def __init__(self, parent):
        super(Actualizacion, self).__init__(parent)
        icono = QIcon(recursos.ICONOS['icono'])
        self.setIcon(icono)
        self.menu_()
        self.version_ = '0'
        self.link = ''

        self.hilo = Hilo()
        self.connect(self.hilo, SIGNAL("versionEdis(QString, QString)"),
                     self.mostrar_mensaje)
        self.hilo.start()

    def menu_(self, descargas=False):
        self.menu = QMenu()
        if descargas:
            self.descarga = QAction(self.tr(u'Versión: %1').arg(
                self.version_), self, triggered=self.mostrar_descarga)
            self.menu.addAction(self.descarga)
            self.menu.addSeparator()
        self.salir = QAction(self.tr(u'Cerrar'), self, triggered=self.hide)
        self.menu.addAction(self.salir)
        self.setContextMenu(self.menu)

    def mostrar_mensaje(self, version_, link):
        self.version_ = str(version_)
        self.link = str(link)
        version_local = version.LooseVersion(interfaz.__version__)
        version_web = version.LooseVersion(self.version_)
        if version_local < version_web:
            if self.supportsMessages():
                self.menu_(True)
                self.showMessage(self.trUtf8("EDIS - Actualización!"),
                                 self.trUtf8("Nueva versión disponible: ") +
                                 self.version_ +
                                 self.trUtf8("\nClick en el ícono para ir "
                                             "a la web!"),
                                 QSystemTrayIcon.Information, 10000)
            else:
                boton = QMessageBox.information(self.parent(),
                                                self.tr("EDIS - Actualizar!"),
                                                self.tr("Nueva version "
                                                        "disponible: ") +
                                                self.version_)
                if boton == QMessageBox.Ok:
                    self.mostrar_descarga()
        else:
            self.hide()

    def mostrar_descarga(self):
        webbrowser.open(self.link)
        self.hide()


class Hilo(QThread):

    def __init__(self):
        super(Hilo, self).__init__()

    def run(self):
        edis = {}
        try:
            version_ = urllib.urlopen(interfaz.__actualizar__)
            edis = parsear(version_)
        except:
            print("No hay conexión a la red!")
        self.emit(SIGNAL("versionEdis(QString, QString)"),
                  edis.get('version', '0'), edis.get('descarga', ''))


def parsear(version_):
    try:
        return json.load(version_)
    except:
        return {}
