# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence

# Módulos QtCore
from PyQt4.QtCore import Qt

from src.ui.contenedores.output import procesos


class ContenedorOutput(QWidget):

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