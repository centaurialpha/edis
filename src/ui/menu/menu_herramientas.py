#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

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

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from src import recursos
from src.ui.editor import acciones_
from src.ui.widgets.creador_widget import crear_accion

_ICONO = recursos.ICONOS


class MenuHerramientas(QObject):

    def __init__(self, menu_herramientas, toolbar, ide):
        super(MenuHerramientas, self).__init__()

        self.ide = ide
        #TODO:
        #FIXME:
        # Acciones #
        # Insertar título
        accionTitulo = crear_accion(self, "Insertar título",
            slot=self.insertar_titulo)
        menu_herramientas.addAction(accionTitulo)
        # Insertar separador
        accionSeparador = crear_accion(self, "Insertar separador",
            icono=_ICONO['separador'], slot=self.insertar_separador)
        menu_herramientas.addAction(accionSeparador)
        # Insertar include
        accionInclude = crear_accion(self, "Insertar '#include'",
            icono=_ICONO['include'],
            slot=self.ide.distribuidor.insertar_include)
        menu_herramientas.addAction(accionInclude)
        accionInsertarMacro = crear_accion(self, "Insertar '#define'",
            icono=_ICONO['macro'], slot=self.insertar_macro)
        menu_herramientas.addAction(accionInsertarMacro)
        menu_herramientas.addSeparator()
        # Insertar fecha y hora
        menu_fecha_hora = menu_herramientas.addMenu(
            self.trUtf8("Insertar fecha y hora"))
        accionDMA = menu_fecha_hora.addAction(
            self.trUtf8("dd-mm-aaaa"))
        accionMDA = menu_fecha_hora.addAction(
            self.trUtf8("mm-dd-aaaa"))
        accionAMD = menu_fecha_hora.addAction(
            self.trUtf8("aaaa-mm-dd"))
        menu_fecha_hora.addSeparator()
        accionDMAH = menu_fecha_hora.addAction(
            self.trUtf8("dd-mm-aaaa hh:mm"))
        accionMDAH = menu_fecha_hora.addAction(
            self.trUtf8("mm-dd-aaaa hh:mm"))
        accionAMDH = menu_fecha_hora.addAction(
            self.trUtf8("aaaa-mm-dd hh:mm"))
        menu_herramientas.addSeparator()

        # Toolbar #
        self.items_toolbar = {
            #"linea": accionSeparador,
            #"macro": accionInsertarMacro,
            #"include": accionInclude,
            }

        # Conexión
        accionDMA.triggered.connect(lambda x: self._insertar_fecha(1))
        accionMDA.triggered.connect(lambda x: self._insertar_fecha(2))
        accionAMD.triggered.connect(lambda x: self._insertar_fecha(3))
        accionDMAH.triggered.connect(lambda h: self._insertar_fecha_hora(1))
        accionMDAH.triggered.connect(lambda h: self._insertar_fecha_hora(2))
        accionAMDH.triggered.connect(lambda h: self._insertar_fecha_hora(3))

    def insertar_separador(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW:
            acciones_.insertar_linea(editorW)

    def insertar_titulo(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW:
            acciones_.insertar_titulo(editorW)

    def _insertar_fecha(self, formato):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW:
            acciones_.insertar_fecha(editorW, formato)

    def _insertar_fecha_hora(self, formato):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW:
            acciones_.insertar_fecha_hora(editorW, formato)

    def insertar_macro(self):
        self.ide.distribuidor.insertar_macro()