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

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

from edis_c.interfaz.editor import acciones_
from edis_c import recursos
from edis_c import traducciones as tr


class MenuArchivo(QObject):
    """ Items del menú Archivo """

    def __init__(self, menu_archivo, toolbar, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide

        # Se cargan los shortcut #

        self.atajoNuevo = QShortcut(recursos.ATAJOS['nuevo'], self.ide)
        self.atajoAbrir = QShortcut(recursos.ATAJOS['abrir'], self.ide)
        self.atajoGuardar = QShortcut(recursos.ATAJOS['guardar'], self.ide)
        self.atajoImprimir = QShortcut(recursos.ATAJOS['imprimir'], self.ide)
        self.atajoCerrarTab = QShortcut(recursos.ATAJOS['cerrar-tab'], self.ide)

        # Conexiones
        self.connect(self.atajoNuevo, SIGNAL("activated()"),
            self.ide.contenedor_principal.agregar_editor)
        self.connect(self.atajoAbrir, SIGNAL("activated()"),
            self.ide.contenedor_principal.abrir_archivo)
        self.connect(self.atajoGuardar, SIGNAL("activated()"),
            self.ide.contenedor_principal.guardar_archivo)
        self.connect(self.atajoCerrarTab, SIGNAL("activated()"),
            self.ide.contenedor_principal.cerrar_tab)
        self.connect(self.atajoImprimir, SIGNAL("activated()"),
            self.imprimir_)

        # Acciones #
        # Nuevo
        self.accionNuevo = menu_archivo.addAction(
            QIcon(recursos.ICONOS['nuevo']), self.trUtf8(tr.TRAD_NUEVO))
        self.cargar_status_tip(self.accionNuevo,
            self.trUtf8("Crear un archivo nuevo"))
        # Nuevo desde plantilla
        self.accionNuevoDesdePlantilla = menu_archivo.addMenu(
            tr.TRAD_NUEVO_PLANTILLA)
        menu_archivo.addSeparator()
        self.accionNuevoMain = self.accionNuevoDesdePlantilla.addAction(
            QIcon(recursos.ICONOS['main']), tr.TRAD_NUEVO_MAIN)
        self.cargar_status_tip(self.accionNuevoMain,
            self.trUtf8("Crear un nuevo archivo de C con función main"))
        # Abrir
        self.accionAbrir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['abrir']), tr.TRAD_ABRIR)
        self.cargar_status_tip(self.accionAbrir,
            self.trUtf8("Abrir cualquier archivo de tipo C (.c .h .cpp)"))
        menu_archivo.addSeparator()
        # Guardar
        self.accionGuardar = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar']), tr.TRAD_GUARDAR)
        self.cargar_status_tip(self.accionGuardar,
            self.trUtf8("Guardar cambios en el archivo actual"))
        # Guardar como
        self.accionGuardarComo = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar-como']), tr.TRAD_GUARDAR_COMO)
        self.cargar_status_tip(self.accionGuardarComo,
            self.trUtf8("Elegir dónde guardar archivo actual"))
        # Guardar todo
        self.accionGuardarTodo = menu_archivo.addAction(tr.TRAD_GUARDAR_TODO)
        menu_archivo.addSeparator()
        # Imprimir
        self.accionImprimir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['print']), tr.TRAD_IMPRIMIR)
        self.cargar_status_tip(self.accionImprimir,
            self.trUtf8("Imprimir código fuente"))
        # Exportar a PDF
        self.accionExportarComoPDF = menu_archivo.addAction(
            self.trUtf8("Exportar a PDF"))
        menu_archivo.addSeparator()
        # Cerrar
        self.accionCerrarTab = menu_archivo.addAction(tr.TRAD_CERRAR)
        self.cargar_status_tip(self.accionCerrarTab,
            self.trUtf8("Cerrar pestaña actual"))
        # Cerrar todo
        self.accionCerrarTodo = menu_archivo.addAction(tr.TRAD_CERRAR_TODO)
        self.cargar_status_tip(self.accionCerrarTodo,
            self.trUtf8("Cerrar todas las pestañas"))
        # Cerrar todo excepto actual
        self.accionCerrarExceptoActual = menu_archivo.addAction(
            tr.TRAD_CERRAR_EXC)
        self.cargar_status_tip(self.accionCerrarExceptoActual,
            self.trUtf8("Cerrar todas las pestañas excepto actual"))
        menu_archivo.addSeparator()
        # Salir
        self.accionSalir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['salir']), tr.TRAD_SALIR)
        self.cargar_status_tip(self.accionSalir,
            self.trUtf8("Salir de EDIS-C"))

        # Conexión a métodos #
        self.accionNuevo.triggered.connect(
            self.ide.contenedor_principal.agregar_editor)
        self.accionNuevoMain.triggered.connect(
            self.archivo_main_c)
        self.accionAbrir.triggered.connect(
            self.ide.contenedor_principal.abrir_archivo)
        self.accionGuardar.triggered.connect(
            self.ide.contenedor_principal.guardar_archivo)
        self.accionGuardarComo.triggered.connect(
            self.ide.contenedor_principal.guardar_archivo_como)
        self.accionGuardarTodo.triggered.connect(
            self.ide.contenedor_principal.guardar_todo)
        self.accionImprimir.triggered.connect(
            self.imprimir_)
        self.accionCerrarTab.triggered.connect(
            self.ide.contenedor_principal.cerrar_tab)
        self.accionCerrarExceptoActual.triggered.connect(
            self.ide.contenedor_principal.cerrar_excepto_actual)
        self.accionCerrarTodo.triggered.connect(
            self.ide.contenedor_principal.cerrar_todo)
        self.accionSalir.triggered.connect(
            self.ide.close)

        # Toolbar #
        self.items_toolbar = {
            "nuevo-archivo": self.accionNuevo,
            "abrir-archivo": self.accionAbrir,
            "guardar-archivo": self.accionGuardar,
            "guardar-como-archivo": self.accionGuardarComo
            }

    def cargar_status_tip(self, accion, texto):
        self.ide.cargar_status_tips(accion, texto)

    def imprimir_(self):
        """ Llama al método para imprimir archivo actual """

        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW is not None:
            nombre = "Documento_nuevo.pdf"

            acciones_.imprimir_archivo(nombre, editorW.print_)
        return False

    def archivo_main_c(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW is not None:
            acciones_.nuevo_main_c(editorW)