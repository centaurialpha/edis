# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QListWidget,
    )


class Navegador(QListWidget):

    def __init__(self):
        super(Navegador, self).__init__()

    def agregar(self, archivo):
        self.addItem(archivo)

    def eliminar(self, indice):
        self.takeItem(indice)
