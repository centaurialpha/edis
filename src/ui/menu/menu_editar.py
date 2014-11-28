#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

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

# Módulos QtGui
from PyQt4.QtGui import (
    QToolButton,
    QIcon
    )

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from src import recursos
from src.ui.dialogos.preferencias import preferencias
from src.ui.editor import acciones_
from src.ui.widgets.creador_widget import crear_accion

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
            icono=_ICONO['undo'], atajo=_ATAJO['deshacer'],
            slot=self.ide.contenedor_principal.deshacer)
        # Rehacer
        self.accionRehacer = crear_accion(self, "Rehacer",
            icono=_ICONO['redo'], atajo=_ATAJO['rehacer'],
            slot=self.ide.contenedor_principal.rehacer)
        # Cortar
        self.accionCortar = crear_accion(self, "Cortar", icono=_ICONO['cut'],
            atajo=_ATAJO['cortar'], slot=self.ide.contenedor_principal.cortar)
        # Copiar
        self.accionCopiar = crear_accion(self, "Copiar", icono=_ICONO['copy'],
            atajo=_ATAJO['copiar'], slot=self.ide.contenedor_principal.copiar)
        # Pegar
        self.accionPegar = crear_accion(self, "Pegar", icono=_ICONO['paste'],
            atajo=_ATAJO['pegar'], slot=self.ide.contenedor_principal.pegar)
        # Indentar más
        self.accionIndentar = crear_accion(self, "Indentar",
            icono=_ICONO['indent'], atajo=_ATAJO['indentar'],
            slot=self.ide.contenedor_principal.indentar_mas)
        # Indentar menos
        self.accionQuitarIndentacion = crear_accion(self, "Quitar indentación",
            icono=_ICONO['unindent'],
            atajo=_ATAJO['quitar-indentacion'],
            slot=self.ide.contenedor_principal.indentar_menos)
        # Seleccionar todo
        self.accionSeleccionarTodo = crear_accion(self, "Seleccionar todo",
            atajo=_ATAJO['seleccionar'], icono=_ICONO['select-all'],
            slot=self.ide.contenedor_principal.seleccionar_todo)
        # Mover hacia arriba
        self.accionMoverArriba = crear_accion(self, "Mover hacia arriba",
            icono=_ICONO['go-up'], atajo=_ATAJO['mover-arriba'],
            slot=self.mover_linea_hacia_arriba)
        # Mover hacia abajo
        self.accionMoverAbajo = crear_accion(self, "Mover hacia abajo",
            icono=_ICONO['go-down'], atajo=_ATAJO['mover-abajo'],
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
            atajo=_ATAJO['titulo'], slot=self.convertir_a_titulo)
        menu_editar.addSeparator()
        # Eliminar línea
        self.accionEliminarLinea = crear_accion(self, "Eliminar línea",
            atajo=_ATAJO['eliminar'], slot=self.eliminar_linea)
        # Duplicar línea
        self.accionDuplicarLinea = crear_accion(self, "Duplicar línea",
            self.duplicar_linea, atajo=_ATAJO['duplicar'],
            slot=self.duplicar_linea)
        # Comentar
        self.accionComentar = crear_accion(self, "Comentar",
            atajo=_ATAJO['comentar'], slot=self.comentar)
        # Descomentar
        self.accionDescomentar = crear_accion(self, "Descomentar",
            atajo=_ATAJO['descomentar'], slot=self.descomentar)
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

        self.tool_deshacer = QToolButton()
        self.tool_deshacer.setDefaultAction(self.accionDeshacer)
        #self.tool_deshacer.setIcon(QIcon(_ICONO['undo']))

        self.tool_rehacer = QToolButton()
        self.tool_rehacer.setDefaultAction(self.accionRehacer)
        #self.tool_rehacer.setIcon(QIcon(_ICONO['re']))

        # Items de la barra de herramientas
        self.items_toolbar = {
            "deshacer": self.tool_deshacer,
            "rehacer": self.tool_rehacer,
            #"cortar": self.accionCortar,
            #"copiar": self.accionCopiar,
            #"pegar": self.accionPegar,
            #"indentar": self.accionIndentar,
            #"desindentar": self.accionQuitarIndentacion,
            #"arriba": self.accionMoverArriba,
            #"abajo": self.accionMoverAbajo
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
        self.preferencias = preferencias.Preferencias(self.ide)
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