# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow
    )

# Módulos QtCore

# Módulos EDIS
from src import ui
from src.ui.contenedores import principal
from src.ui.lateral_widget import lateral_container
from src.ui.contenedor_secundario import contenedor_secundario


class EDIS(QMainWindow):
    """
    Esta clase es conocedora de todas las demás.

    """

    # Cada instancia de una clase  se guarda en éste diccionario
    __COMPONENTES = {}

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(ui.__nombre__)
        self.setMinimumSize(750, 500)
        # Widget central
        self.central = EDIS.componente("central")
        self.cargar_contenedores(self.central)
        self.setCentralWidget(self.central)
        # Barra de estado
        self.barra_de_estado = EDIS.componente("barra_de_estado")
        self.setStatusBar(self.barra_de_estado)

    @classmethod
    def cargar_componente(cls, nombre, instancia):
        """ Se guarda el nombre y la instancia de una clase """

        cls.__COMPONENTES[nombre] = instancia

    @classmethod
    def componente(cls, nombre):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTES.get(nombre, None)

    def cargar_contenedores(self, central):
        self.contenedor_editor = principal.EditorContainer(self)
        self.contenedor_output = contenedor_secundario.ContenedorSecundario(self)
        self.contenedor_lateral = lateral_container.LateralContainer(self)

        central.agregar_contenedor_lateral(self.contenedor_lateral)
        central.agregar_contenedor_editor(self.contenedor_editor)
        central.agregar_contenedor_output(self.contenedor_output)