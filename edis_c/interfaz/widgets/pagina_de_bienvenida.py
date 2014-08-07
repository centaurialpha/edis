#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

# Módulos Python
import os
from urlparse import urlparse, urlunparse

# Módulos QtGui
from PyQt4 import QtGui

# Módulos QtCore
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import SIGNAL
from PyQt4.QtDeclarative import QDeclarativeView

# Módulos EDIS
import edis_c
from edis_c import recursos


class PaginaDeBienvenida(QtGui.QWidget):

    def __init__(self, parent=None):
        super(PaginaDeBienvenida, self).__init__(parent)
        self._id = edis_c.__nombre__
        vbox = QtGui.QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.ver = QDeclarativeView()
        self.ver.setMinimumWidth(400)
        self.ver.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        qml = unicode(QDir.fromNativeSeparators(os.path.join(
            recursos.PAGINA_INICIO, "pagina_de_bienvenida.qml")))
        path_qml = urlunparse(urlparse(qml)._replace(scheme='file'))
        self.ver.setSource(QUrl(path_qml))
        self.root = self.ver.rootObject()
        vbox.addWidget(self.ver)

        self.connect(self.root, SIGNAL("nuevoArchivo()"),
            lambda: self.emit(SIGNAL("nuevoArchivo()")))
        self.connect(self.root, SIGNAL("abrirArchivo()"),
            lambda: self.emit(SIGNAL("abrirArchivo()")))