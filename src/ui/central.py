# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    #QSplitter,
    #QVBoxLayout,
    )

#from PyQt4.QtCore import QObject

from src.ui.edis_main import EDIS


class Central(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        EDIS.cargar_componente("central", self)

    def agregar_contenedor_editor(self, contenedor):
        pass

    def agregar_contenedor_output(self, contenedor):
        pass

    def agregar_contenedor_lateral(self, contenedor):
        pass


central = Central()
#class Central(QWidget):

    #def __init__(self):
        #QWidget.__init__(self)

        #box = QVBoxLayout(self)
        #box.setContentsMargins(0, 0, 0, 0)

        ## Splitters
        #self.splitter_principal = QSplitter(Qt.Vertical)
        #self.splitter_secundario = QSplitter(Qt.Horizontal)

        #box.addWidget(self.splitter_secundario)
        #EDIS.cargar_componente("central", self)

    #def agregar_contenedor_editor(self, contenedor):
        #""" Agrega el contenedor del editor en el centro """

        #self.contenedor_editor = contenedor
        #self.splitter_principal.addWidget(contenedor)

    #def agregar_contenedor_lateral(self, contenedor):
        #""" Agrega el contenedor lateral a la izquierda """

        #self.lateral = contenedor
        #self.splitter_secundario.addWidget(contenedor)

    #def agregar_contenedor_output(self, contenedor):
        #""" Agrega el contenedor de la salida del compilador """

        #self.output = contenedor
        #self.output.hide()
        #self.splitter_principal.addWidget(contenedor)

    #def showEvent(self, e):
        #super(Central, self).showEvent(e)
        #self.splitter_secundario.insertWidget(1, self.splitter_principal)
        #self.splitter_principal.setSizes([900, 300])
        #self.splitter_secundario.setSizes([self.width() / 4, self.width()])


#central = Central()