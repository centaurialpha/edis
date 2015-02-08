# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    #QRadioButton,
    QSpacerItem,
    QSizePolicy
    )

from src.helpers import (
    configuracion,
    #comprobar_terminales
    )
from src.helpers.configuracion import ESettings

#FIXME:


class ConfiguracionEjecucion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEjecucion, self).__init__()
        box = QVBoxLayout(self)
        layout_radio = QVBoxLayout()
        #self.buscar_terminal()

        #for i in self.radio_terminales:
            #layout_radio.addWidget(i)
            #if i.text() == configuracion.ESettings.get('terminal'):
                #i.setChecked(True)

        #box.addLayout(layout_radio)
        #box.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                    #QSizePolicy.Expanding))

    def buscar_terminal(self):
        self.radio_terminales = []
        #terminales = comprobar_terminales.comprobar()
        #[self.radio_terminales.append(QRadioButton(terminal))
            #for terminal in terminales]

    def guardar(self):
        pass
        #terminal = ""
        #for i in self.radio_terminales:
            #if i.isChecked():
                #terminal = i.text()
        #ESettings.set('terminal', terminal)