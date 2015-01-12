# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtCore import QObject

from src.ui.menu import acciones
from src.ui.edis_main import EDIS

#FIXME: Se podría mejorar


class Menu(QObject):

    def __init__(self):
        QObject.__init__(self)
        # QActions
        self.acciones = list()

        for accion in acciones.ACCIONES:
            nombre = accion.get("nombre")
            conexion = accion.get("conexion")
            atajo = accion.get("atajo", None)
            icono = accion.get("icono", None)
            seccion = accion.get("seccion")
            separador = accion.get("separador", False)
            submenu = accion.get("submenu", False)
            checkable = accion.get("checkable", False)
            qaccion = Accion(nombre, conexion, seccion, icono, atajo)
            qaccion.separador = separador
            qaccion.submenu = submenu
            qaccion.checkable = checkable
            self.acciones.append(qaccion)

        EDIS.cargar_componente("menu", self)


class Accion(object):

    """ Esta clase representa a una acción (QAction) """

    def __init__(self, nombre, conexion, seccion, icono=None, atajo=None):
        self.nombre = nombre
        self.conexion = conexion
        self.seccion = seccion
        self.icono = icono
        self.atajo = atajo
        self.separador = False
        self.submenu = False
        self.checkable = False

menu = Menu()