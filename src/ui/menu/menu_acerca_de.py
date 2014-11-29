# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

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
from src import ui
from src import recursos
#from src.ui.widgets import estilo
from src.ui.dialogos import dialogo_acerca_de_ide
#from src.ui.contenedor_principal import contenedor_principal
from src.ui.widgets.creador_widget import crear_accion

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
            icono=_ICONO['help'], slot=self.acerca_de_ide)
        menu_acerca_de.addAction(acerca_ide)
        acerca_qt = crear_accion(self, "Acerca de Qt",
            icono=_ICONO['qt'], slot=self.acerca_de_qt)
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
        webbrowser.open(ui.__reportar_bug__)

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