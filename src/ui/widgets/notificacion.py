# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
from urlparse import urlparse, urlunparse
import os

# Módulos QtGui
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QVBoxLayout

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QDir
from PyQt4.QtCore import SIGNAL
from PyQt4.QtDeclarative import QDeclarativeView

# Módulos EDIS
from src.herlpers import configuraciones
from src import recursos


class Notificacion(QFrame):

    def __init__(self, parent=None):
        super(Notificacion, self).__init__(None, Qt.ToolTip)
        self.parent = parent
        self.duracion = 3000
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: transparent")
#        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedHeight(25)

        ver = QDeclarativeView()
        ver.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        qml = unicode(QDir.fromNativeSeparators(os.path.join(
            recursos.NOTIFICACION, "notificacion.qml")))
        path_qml = urlunparse(urlparse(qml)._replace(scheme='file'))
        ver.setSource(QUrl(path_qml))
        self.root = ver.rootObject()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        # Fondo frame
        vbox.addWidget(ver)

        #self.root.close.connect(self.close)
        self.connect(self.root, SIGNAL("close()"), self.close)

    def showEvent(self, evento):
        super(Notificacion, self).showEvent(evento)
        width, pgeo = self.parent.width(), self.parent.geometry()
        condi_vertical = configuraciones.POSS in (0, 1)
        condi_horizontal = configuraciones.POSS in (0, 2)
        x = pgeo.left() if condi_horizontal else pgeo.right()
        y = (pgeo.bottom() - self.height()
            if condi_vertical else pgeo.top())
        self.setFixedWidth(width)
        self.setGeometry(x, y, self.width(), self.height())
        fondo = ('#bbbbbb')
        fore = ('#111')
        self.root.setColor(fondo, fore)
        self.root.start(self.duracion)

    def set_message(self, text='', duracion=7000):
        self.root.setText(text)
        self.duracion = duracion
