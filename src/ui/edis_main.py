# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow,
    )

# Módulos QtCore

# Módulos EDIS
from src import ui
from src.ui.contenedores import principal
from src.ui.contenedores.lateral import lateral_container
from src.ui.contenedores.output import contenedor_secundario
from src.ui.menu.menu_archivo import MenuArchivo
#lint:disable
#from src.ui.menu import menu_archivo
#lint:enable


class EDIS(QMainWindow):
    """
    Esta clase es conocedora de todas las demás.

    """

    # Cada instancia de una clase  se guarda en éste diccionario
    __COMPONENTES = {}
    __MENUBAR = {}  # Nombre de los menus

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(ui.__nombre__)
        self.setMinimumSize(750, 500)
        # Menú
        #FIXME: Modificar la creación de menú
        EDIS.menu_bar(0, self.trUtf8("&Archivo"))
        EDIS.menu_bar(1, self.trUtf8("&Editar"))
        EDIS.menu_bar(2, self.trUtf8("&Ver"))
        EDIS.menu_bar(3, self.trUtf8("&Buscar"))
        EDIS.menu_bar(4, self.trUtf8("&Herramientas"))
        EDIS.menu_bar(5, self.trUtf8("E&jecución"))
        EDIS.menu_bar(6, self.trUtf8("A&cerca de"))

        # Widget central
        self.central = EDIS.componente("central")
        self.cargar_contenedores(self.central)
        self.setCentralWidget(self.central)

        menu = self.menuBar()
        menu_archivo = menu.addMenu("&Archivo")
        self.menu_archivo = MenuArchivo(menu_archivo, self)

    @classmethod
    def cargar_componente(cls, nombre, instancia):
        """ Se guarda el nombre y la instancia de una clase """

        cls.__COMPONENTES[nombre] = instancia

    @classmethod
    def componente(cls, nombre):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTES.get(nombre, None)

    @classmethod
    def menu_bar(cls, clave, nombre):
        """ Se guarda el nombre de cada menú """

        cls.__MENUBAR[clave] = nombre

    @classmethod
    def get_menu(cls, clave):
        """ Devuelve un diccionario con los menu """

        return cls.__MENUBAR.get(clave, None)

    def cargar_contenedores(self, central):
        """ Carga los 3 contenedores (editor, lateral y output """

        self.contenedor_editor = principal.EditorContainer(self)
        self.contenedor_output = contenedor_secundario.ContenedorOutput(self)
        self.contenedor_lateral = lateral_container.LateralContainer(self)

        # Agrego los contenedores al widget central
        central.agregar_contenedor_lateral(self.contenedor_lateral)
        central.agregar_contenedor_editor(self.contenedor_editor)
        central.agregar_contenedor_output(self.contenedor_output)