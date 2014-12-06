# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QComboBox
    )

from PyQt4.QtCore import Qt

from src.ui.edis_main import EDIS


class Central(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        box = QVBoxLayout(self)
        # Splitters

        self.splitter_principal = QSplitter(Qt.Vertical)
        self.splitter_secundario = QSplitter(Qt.Horizontal)

        box.addWidget(self.splitter_secundario)
        #box.addLayout(box)
        EDIS.cargar_componente("central", self)

    def agregar_contenedor_editor(self, contenedor):
        """ Agrega el contenedor del editor en el centro """

        self.contenedor_editor = contenedor
        self.splitter_principal.addWidget(contenedor)

    def agregar_contenedor_lateral(self, contenedor):
        """ Agrega el contenedor lateral a la izquierda """

        self.lateral = contenedor
        self.splitter_secundario.addWidget(contenedor)

    def agregar_contenedor_output(self, contenedor):
        """ Agrega el contenedor de la salida del compilador """

        self.output = contenedor
        self.splitter_principal.addWidget(contenedor)

    def showEvent(self, e):
        super(Central, self).showEvent(e)
        self.splitter_secundario.insertWidget(1, self.splitter_principal)
        tamaño_principal = [self.height(), self.height() / 3]
        tamaño_secundario = [self.width() / 5, self.width()]
        self.splitter_principal.setSizes(tamaño_principal)
        self.splitter_secundario.setSizes(tamaño_secundario)


central = Central()