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
    QToolButton,
    QMenu,
    QSizePolicy
    )

# Módulos QtCore
from PyQt4.QtCore import (
    QObject,
    SIGNAL
    )

# Módulos EDIS
from src.ui.editor import (
    acciones_,
    editor
    )
from src import recursos
from src.helpers import configuraciones
from src import traducciones as tr
from src.ui.widgets.creador_widget import (
    crear_accion,
    create_button
    )
#from src.ui.dialogos import dialogo_proyecto

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
        self.accionNuevo = crear_accion(self, "Nuevo", icono=_ICONO['new'],
            atajo=_ATAJO['nuevo'],
            slot=self.ide.contenedor_principal.agregar_editor)
        ## Nuevo desde plantilla
        self.accionNuevoMain = crear_accion(self, "Nuevo main",
            icono=_ICONO['c'], slot=self.archivo_main_c)
        # Abrir
        self.accionAbrir = crear_accion(self, "Abrir", icono=_ICONO['open'],
            atajo=_ATAJO['abrir'],
            slot=self.ide.contenedor_principal.abrir_archivo)
        # Guardar
        self.accionGuardar = crear_accion(self, "Guardar",
            icono=_ICONO['save'], atajo=_ATAJO['guardar'],
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
        # Propiedades
        self.accion_propiedades = crear_accion(self, "Propiedades",
            slot=self.ide.distribuidor.file_property)
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
        menu_archivo.addAction(self.accion_propiedades)
        menu_archivo.addAction(self.accionExportarComoPDF)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionCerrarTab)
        menu_archivo.addAction(self.accionCerrarTodo)
        menu_archivo.addAction(self.accionCerrarExceptoActual)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accionSalir)

        # ToolButton's
        self.tool_nuevo = create_button(self.ide, shortcut=_ATAJO['nuevo'],
            action=self.accionNuevo, text=self.tr("Nuevo"))
        self.tool_nuevo.setSizePolicy(QSizePolicy.MinimumExpanding,
            QSizePolicy.Maximum)

        self.tool_abrir = create_button(self.ide, shortcut=_ATAJO['abrir'],
            action=self.accionAbrir, text=self.tr("Abrir"))
        self.tool_abrir.setSizePolicy(QSizePolicy.MinimumExpanding,
            QSizePolicy.Maximum)
        self.tool_abrir.setPopupMode(QToolButton.InstantPopup)

        self.tool_guardar = create_button(self.ide, shortcut=_ATAJO['guardar'],
            action=self.accionGuardar, text=self.tr("Guardar"))
        self.tool_guardar.setSizePolicy(QSizePolicy.MinimumExpanding,
            QSizePolicy.Maximum)
        self.tool_guardar.setPopupMode(QToolButton.InstantPopup)
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