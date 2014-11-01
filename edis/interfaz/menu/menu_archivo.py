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
    QMessageBox,
    QIcon,
    QToolButton,
    QMenu
    )

# Módulos QtCore
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

# Módulos EDIS
from edis.interfaz.editor import acciones_
from edis.interfaz.editor import editor
from edis import recursos
from edis.nucleo import configuraciones
from edis import traducciones as tr
from edis.interfaz.widgets.creador_widget import crear_accion
#from edis.interfaz.dialogos import dialogo_proyecto

_ICONO = recursos.ICONOS
_ATAJO = recursos.ATAJOS


class MenuArchivo(QObject):
    """ Items del menú Archivo """

    def __init__(self, menu_archivo, toolbar, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide
        self.list_archivos = []

        # Acciones #
        # Nuevo
        self.accionNuevo = crear_accion(self, "Nuevo", icono=_ICONO['nuevo'],
            atajo=_ATAJO['nuevo'],
            slot=self.ide.contenedor_principal.agregar_editor)
        ## Nuevo desde plantilla
        self.accionNuevoMain = crear_accion(self, "Nuevo main",
            icono=_ICONO['c'], slot=self.archivo_main_c)
        # Abrir
        self.accionAbrir = crear_accion(self, "Abrir", icono=_ICONO['abrir'],
            atajo=_ATAJO['abrir'],
            slot=self.ide.contenedor_principal.abrir_archivo)
        # Guardar
        self.accionGuardar = crear_accion(self, "Guardar",
            icono=_ICONO['guardar'], atajo=_ATAJO['guardar'],
            slot=self.ide.contenedor_principal.guardar_archivo)
        # Guardar como
        self.accionGuardarComo = crear_accion(self, "Guardar como",
            icono=_ICONO['guardar-como'],
            slot=self.ide.contenedor_principal.guardar_archivo_como)
        # Guardar todo
        self.accionGuardarTodo = crear_accion(self, "Guardar todo",
            icono=_ICONO['guardar-todo'],
            slot=self.ide.contenedor_principal.guardar_todo)
        # Imprimir
        self.accionImprimir = crear_accion(self, "Imprimir",
            icono=_ICONO['imprimir'], atajo=_ATAJO['imprimir'],
            slot=self.ide.distribuidor.imprimir_documento)
        # Exportar a PDF
        self.accionExportarComoPDF = crear_accion(self, "Exportar a PDF",
            icono=_ICONO['exportar'],
            slot=self.ide.distribuidor.exportar_como_pdf)
        # Cerrar
        self.accionCerrarTab = crear_accion(self, "Cerrar",
            icono=_ICONO['cerrar'], atajo=_ATAJO['cerrar-tab'],
            slot=self.ide.contenedor_principal.cerrar_tab)
        # Cerrar todo
        self.accionCerrarTodo = crear_accion(self, "Cerrar todo",
            slot=self.ide.contenedor_principal.cerrar_todo)
        # Cerrar todo excepto actual
        self.accionCerrarExceptoActual = crear_accion(self,
            "Cerrar todo excepto actual",
            slot=self.ide.contenedor_principal.cerrar_excepto_actual)
        # Salir
        self.accionSalir = crear_accion(self, "Salir", icono=_ICONO['cerrar'],
            slot=self.ide.close)

        # Agregar acciones #
        menu_archivo.addAction(self.accionNuevo)
        self.accionNuevoDesdePlantilla = menu_archivo.addMenu(
            tr.TRAD_NUEVO_PLANTILLA)
        menu_archivo.addSeparator()
        self.accionNuevoDesdePlantilla.addAction(self.accionNuevoMain)
        menu_archivo.addAction(self.accionAbrir)
        # Archivos recientes
        self.archivos_recientes = menu_archivo.addMenu(
            self.trUtf8("Archivos recientes"))
        self.connect(self.archivos_recientes, SIGNAL("triggered(QAction*)"),
            self._abrir_archivo)

        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionGuardar)
        menu_archivo.addAction(self.accionGuardarComo)
        menu_archivo.addAction(self.accionGuardarTodo)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionImprimir)
        menu_archivo.addAction(self.accionExportarComoPDF)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionCerrarTab)
        menu_archivo.addAction(self.accionCerrarTodo)
        menu_archivo.addAction(self.accionCerrarExceptoActual)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionSalir)

        # ToolButton's
        self.tool_nuevo = QToolButton()
        self.tool_nuevo.setIcon(QIcon(_ICONO['nuevo']))
        self.tool_nuevo.setDefaultAction(self.accionNuevo)

        self.tool_abrir = QToolButton()
        self.tool_abrir.setIcon(QIcon(_ICONO['abrir']))
        self.tool_abrir.setPopupMode(QToolButton.MenuButtonPopup)
        self.tool_abrir.setDefaultAction(self.accionAbrir)

        self.tool_guardar = QToolButton()
        self.tool_guardar.setIcon(QIcon(_ICONO['guardar']))
        self.tool_guardar.setDefaultAction(self.accionGuardar)
        self.tool_guardar.setPopupMode(QToolButton.MenuButtonPopup)
        self.tool_guardar.setMenu(self.tool_menu_guardar())

        # Toolbar #
        self.items_toolbar = {
            "nuevo-archivo": self.tool_nuevo,
            "abrir-archivo": self.tool_abrir,
            "guardar-archivo": self.tool_guardar
            }

    def _abrir_archivo(self, accion):
        path = accion.text()
        self.emit(SIGNAL("abrirArchivo(QString)"), path)

    def actualizar_archivos_recientes(self, archivos):
        self.archivos_recientes.clear()
        for i in range(len(archivos)):
            self.archivos_recientes.addAction(unicode(archivos[i]))
            if unicode(archivos[i]) not in self.list_archivos:
                self.list_archivos.append(unicode(archivos[i]))
                if len(self.list_archivos) > configuraciones.MAX_RECIENTES:
                    self.list_archivos = self.list_archivos[1:]
            self.tool_abrir.setMenu(self.tool_menu_abrir())

    def archivo_main_c(self):
        widget = self.ide.contenedor_principal.devolver_widget_actual()
        if isinstance(widget, editor.Editor):
            acciones_.nuevo_main_c(widget)
            widget.setFocus()
        else:
            QMessageBox.information(widget, self.trUtf8("Información!"),
                self.trUtf8("Primero crea un nuevo archivo!"))
        widget.setFocus()

    def tool_menu_abrir(self):
        menu = QMenu(self.ide)
        for i in self.list_archivos:
            menu.addAction(i)
        self.connect(menu, SIGNAL("triggered(QAction*)"),
            self._abrir_archivo)
        return menu

    def tool_menu_guardar(self):
        menu = QMenu(self.ide)
        menu.addAction(self.accionGuardarComo)
        menu.addAction(self.accionGuardarTodo)
        return menu