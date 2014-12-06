# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QComboBox,
    )


class ComboWidget(QComboBox):

    def __init__(self, parent):
        super(ComboWidget, self).__init__(parent)

    def agregar_item(self, nombre):
        self.addItem(nombre)