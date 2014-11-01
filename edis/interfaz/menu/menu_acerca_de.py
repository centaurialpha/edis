#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

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

"""

menu acerca de

"""

# Módulos Python
import webbrowser

# Módulos QtGui
from PyQt4.QtGui import QMessageBox

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
import edis
from edis import recursos
#from edis.interfaz.widgets import estilo
from edis.interfaz.dialogos import dialogo_acerca_de_ide
#from edis.interfaz.contenedor_principal import contenedor_principal
from edis.interfaz.widgets.creador_widget import crear_accion

_ICONO = recursos.ICONOS


class MenuAcercade(QObject):

    def __init__(self, menu_acerca_de, ide):
        super(MenuAcercade, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide
        reportarBugs = crear_accion(self, "Reportar Bug!",
            icono=_ICONO['bug'], slot=self.reportar_bugs_)
        menu_acerca_de.addAction(reportarBugs)
        menu_acerca_de.addSeparator()
        acerca_ide = crear_accion(self, "Acerca de EDIS",
            icono=_ICONO['acerca-de'], slot=self.acerca_de_ide)
        menu_acerca_de.addAction(acerca_ide)
        acerca_qt = crear_accion(self, "Acerca de Qt",
            icono=_ICONO['acerca-qt'], slot=self.acerca_de_qt)
        menu_acerca_de.addAction(acerca_qt)
        menu_acerca_de.addSeparator()
        estilo_de_codigo = menu_acerca_de.addAction(
            self.trUtf8("Estilo de código"))

        # Conexiones
        #reportarBugs.triggered.connect(self.reportar_bugs_)
        #acerca_ide.triggered.connect(self.acerca_de_ide)
        #acerca_qt.triggered.connect(self.acerca_de_qt)
        estilo_de_codigo.triggered.connect(self.estilo_de_codigo)

    def reportar_bugs_(self):
        webbrowser.open(edis.__reportar_bug__)

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