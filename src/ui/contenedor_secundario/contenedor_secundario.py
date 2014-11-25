#-*- coding: utf-8 -*-

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

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence

# Módulos QtCore
from PyQt4.QtCore import Qt

from src.ui.contenedor_secundario import procesos


class ContenedorSecundario(QWidget):

    instancia = None

    def __new__(clase, *args, **kargs):
        if clase.instancia is None:
            clase.instancia = QWidget.__new__(clase, *args, **kargs)
        return clase.instancia

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.salida_ = procesos.EjecutarWidget()
        box.addWidget(self.salida_)

        # Conexiones
        self.atajoEscape = QShortcut(QKeySequence(Qt.Key_Escape),
            self)
        self.atajoEscape.activated.connect(self.hide)

    def compilar(self, path):
        self.show()
        self.nombre_archivo = path
        self.salida_.correr_compilacion(self.nombre_archivo)
        self.salida_.output.setFoco()

    def ejecutar(self):
        #FIXME: revisar!
        if self.salida_.compilado:
            self.salida_.correr_programa()

    def frenar(self):
        self.salida_.terminar_proceso()