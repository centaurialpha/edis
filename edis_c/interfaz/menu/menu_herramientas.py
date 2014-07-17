#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject

from edis_c import recursos


class MenuHerramientas(QObject):

    def __init__(self, menu_herramientas, toolbar, ide):
        super(MenuHerramientas, self).__init__()

        self.ide = ide

        # Acciones #
        # Insertar título
        accionTitulo = menu_herramientas.addAction(
            QIcon(recursos.ICONOS['titulo']), self.trUtf8("Insertar título"))
        # Insertar separador
        accionSeparador = menu_herramientas.addAction(
            QIcon(recursos.ICONOS['linea']), self.trUtf8("Insertar separador"))
        # Insertar include
        menu_include = menu_herramientas.addMenu(
            self.trUtf8("Insertar '#include'"))
        menu_libreria_estandar = menu_include.addMenu(
            self.trUtf8("Librería estándar"))
        accionStdio = menu_libreria_estandar.addAction(
            self.trUtf8("stdio.h"))
        accionStdlib = menu_libreria_estandar.addAction(
            self.trUtf8("stdlib.h"))
        accionString = menu_libreria_estandar.addAction(
            self.trUtf8("string.h"))
        accionInclude = menu_include.addAction(
            QIcon(recursos.ICONOS['insertar-include']),
            self.trUtf8("#include <...>"))
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

        # Toolbar #
        self.items_toolbar = {
            "linea": accionSeparador,
            "titulo": accionTitulo,
            "include": accionInclude
            }