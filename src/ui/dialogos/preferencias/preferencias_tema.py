# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QLabel


class ConfiguracionTema(QWidget):

    def __init__(self, parent):
        super(ConfiguracionTema, self).__init__(parent)
        layoutV = QVBoxLayout(self)

        self.lista_temas = QListWidget()
        self.lista_temas.addItem("Por defecto")
        self.lista_temas.addItem("Black SIDE")

        label = QLabel(self.trUtf8("Elige un tema:"))

        layoutV.addWidget(label)
        layoutV.addWidget(self.lista_temas)
