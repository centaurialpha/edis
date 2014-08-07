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

"""

menu acerca de

"""
import webbrowser

from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject

import edis_c
#from edis_c.interfaz.widgets import estilo
from edis_c.interfaz.dialogos import dialogo_acerca_de_ide
#from edis_c.interfaz.contenedor_principal import contenedor_principal


class MenuAcercade(QObject):

    def __init__(self, menu_acerca_de, ide):
        super(MenuAcercade, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide
        reportarBugs = menu_acerca_de.addAction(self.trUtf8("Reportar bugs!"))
        menu_acerca_de.addSeparator()
        acerca_ide = menu_acerca_de.addAction(self.tr("Acerca de IDE"))
        acerca_qt = menu_acerca_de.addAction(self.tr("Acerca de Qt"))
        menu_acerca_de.addSeparator()
        estilo_de_codigo = menu_acerca_de.addAction(
            self.trUtf8("Estilo de código"))

        # Conexiones
        reportarBugs.triggered.connect(self.reportar_bugs_)
        acerca_ide.triggered.connect(self.acerca_de_ide)
        acerca_qt.triggered.connect(self.acerca_de_qt)
        estilo_de_codigo.triggered.connect(self.estilo_de_codigo)

    def reportar_bugs_(self):
        webbrowser.open(edis_c.__reportar_bug__)

    def acerca_de_ide(self):
        self.acerca_de = dialogo_acerca_de_ide.AcercaDeIDE()
        self.acerca_de.show()

    def acerca_de_qt(self):
        QMessageBox.aboutQt(self.ide, 'Acerca de Qt')

    def estilo_de_codigo(self):
#        widget = estilo.EstiloDeCodigo()
#        contenedor_principal.ContenedorMain().agregar_tab(widget,
#            self.trUtf8("Estilo de Código"))
        pass