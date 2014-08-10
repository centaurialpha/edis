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

# Módulos QtGui

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from edis_c import recursos
from edis_c.interfaz.dialogos.preferencias import preferencias
from edis_c.interfaz.editor import acciones_
from edis_c.interfaz.widgets.creador_widget import crear_accion

_ICONO = recursos.ICONOS
_ATAJO = recursos.ATAJOS


class MenuEditar(QObject):
    """
        Items del menú Editar

        Estructura del módulo 'crear_accion':
        @parent: parent.
        @icono: ícono.
        @texto: texto.
        @atajo: shorcut.
        @tip: status tip.

    """

    def __init__(self, menu_editar, toolbar, ide):
        super(MenuEditar, self).__init__()

        self.ide = ide

        # Acciones #
        # Deshacer
        self.accionDeshacer = crear_accion(self, "Deshacer",
            icono=_ICONO['deshacer'], atajo=_ATAJO['deshacer'],
            slot=self.ide.contenedor_principal.deshacer)
        # Rehacer
        self.accionRehacer = crear_accion(self, "Rehacer",
            icono=_ICONO['rehacer'], atajo=_ATAJO['rehacer'],
            slot=self.ide.contenedor_principal.rehacer)
        # Cortar
        self.accionCortar = crear_accion(self, "Cortar", icono=_ICONO['cortar'],
            atajo=_ATAJO['cortar'], slot=self.ide.contenedor_principal.cortar)
        # Copiar
        self.accionCopiar = crear_accion(self, "Copiar", icono=_ICONO['copiar'],
            atajo=_ATAJO['copiar'], slot=self.ide.contenedor_principal.copiar)
        # Pegar
        self.accionPegar = crear_accion(self, "Pegar", icono=_ICONO['pegar'],
            atajo=_ATAJO['pegar'], slot=self.ide.contenedor_principal.pegar)
        # Indentar más
        self.accionIndentar = crear_accion(self, "Indentar",
            icono=_ICONO['indentar'], atajo=_ATAJO['indentar'],
            slot=self.ide.contenedor_principal.indentar_mas)
        # Indentar menos
        self.accionQuitarIndentacion = crear_accion(self, "Quitar indentación",
            icono=_ICONO['quitar-indentacion'],
            atajo=_ATAJO['quitar-indentacion'],
            slot=self.ide.contenedor_principal.indentar_menos)
        # Seleccionar todo
        self.accionSeleccionarTodo = crear_accion(self, "Seleccionar todo",
            atajo=_ATAJO['seleccionar'],
            slot=self.ide.contenedor_principal.seleccionar_todo)
        # Mover hacia arriba
        self.accionMoverArriba = crear_accion(self, "Mover hacia arriba",
            icono=_ICONO['arriba'], atajo=_ATAJO['mover-arriba'],
            slot=self.mover_linea_hacia_arriba)
        # Mover hacia abajo
        self.accionMoverAbajo = crear_accion(self, "Mover hacia abajo",
            icono=_ICONO['abajo'], atajo=_ATAJO['mover-abajo'],
            slot=self.mover_linea_hacia_abajo)
        # Convertir a mayúsculas
        self.accionConvertirMayusculas = crear_accion(self,
            "Texto seleccionado: a mayúsculas",
            slot=self.convertir_a_mayusculas)
        # Convertir a minúsculas
        self.accionConvertirMinusculas = crear_accion(self,
            "Texto seleccionado: a minúsculas",
            slot=self.convertir_a_minusculas)
        # Convertir a título
        self.accionTitulo = crear_accion(self, "Convertir a título",
            slot=self.convertir_a_titulo)
        menu_editar.addSeparator()
        # Eliminar línea
        self.accionEliminarLinea = crear_accion(self, "Eliminar línea",
            slot=self.eliminar_linea)
        # Duplicar línea
        self.accionDuplicarLinea = crear_accion(self, "Duplicar línea",
            self.duplicar_linea, slot=self.duplicar_linea)
        # Comentar
        self.accionComentar = crear_accion(self, "Comentar", slot=self.comentar)
        # Descomentar
        self.accionDescomentar = crear_accion(self, "Descomentar",
            slot=self.descomentar)
        menu_editar.addSeparator()
        # Preferencias
        self.accionConfiguracion = crear_accion(self, "Preferencias",
            slot=self._configuraciones)

        # Agregar acciones al menú #
        menu_editar.addAction(self.accionDeshacer)
        menu_editar.addAction(self.accionRehacer)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionCortar)
        menu_editar.addAction(self.accionCopiar)
        menu_editar.addAction(self.accionPegar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionIndentar)
        menu_editar.addAction(self.accionQuitarIndentacion)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionSeleccionarTodo)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionMoverArriba)
        menu_editar.addAction(self.accionMoverAbajo)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionConvertirMayusculas)
        menu_editar.addAction(self.accionConvertirMinusculas)
        menu_editar.addAction(self.accionTitulo)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionEliminarLinea)
        menu_editar.addAction(self.accionDuplicarLinea)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionComentar)
        menu_editar.addAction(self.accionDescomentar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accionConfiguracion)

        # Items de la barra de herramientas
        self.items_toolbar = {
            "deshacer": self.accionDeshacer,
            "rehacer": self.accionRehacer,
            "cortar": self.accionCortar,
            "copiar": self.accionCopiar,
            "pegar": self.accionPegar,
            "indentar": self.accionIndentar,
            "desindentar": self.accionQuitarIndentacion,
            "arriba": self.accionMoverArriba,
            "abajo": self.accionMoverAbajo
            }

    def mover_linea_hacia_arriba(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.mover_hacia_arriba(editor)

    def mover_linea_hacia_abajo(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.mover_hacia_abajo(editor)

    def _configuraciones(self):
        self.preferencias = preferencias.DialogoConfiguracion(self.ide)
        self.preferencias.show()

    def convertir_a_mayusculas(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.convertir_a_mayusculas(editor)

    def convertir_a_minusculas(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.convertir_a_minusculas(editor)

    def convertir_a_titulo(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.convertir_a_titulo(editor)

    def eliminar_linea(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.eliminar_linea(editor)

    def duplicar_linea(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.duplicar_linea(editor)

    def comentar(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.comentar(editor)

    def descomentar(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            acciones_.descomentar(editor)