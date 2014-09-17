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

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos EDIS
from edis_c import recursos
from edis_c.interfaz.widgets.creador_widget import crear_accion

_ATAJO = recursos.ATAJOS
_ICONO = recursos.ICONOS


class MenuVer(QObject):

    def __init__(self, menu_ver, toolbar, ide):
        super(MenuVer, self).__init__()

        self.ide = ide

        # Acciones #
        # Pantalla completa
        self.accionFullScreen = crear_accion(self, "Pantalla completa",
            icono=_ICONO['pantalla-completa'], atajo=_ATAJO['fullscreen'],
            slot=self.pantalla_completa)
        self.accionFullScreen.setCheckable(True)
        # Widget lateral
        self.accionMostrarLateral = crear_accion(self,
            "Mostrar/ocultar navegador", slot=self.ocultar_mostrar_navegador)
        self.accionMostrarLateral.setCheckable(True)
        # Mostrar/ocultar barra de herramientas
        self.accionMostrarOcultarToolbar = crear_accion(self,
            "Mostrar/ocultar barra de herramientas",
            atajo=_ATAJO['ocultar-toolbar'], slot=self.ocultar_mostrar_toolbars)
        self.accionMostrarOcultarToolbar.setCheckable(True)
        # Mostrar/ocultar editor
        self.accionMostrarOcultarEditor = crear_accion(self,
            "Mostrar/ocultar editor", atajo=_ATAJO['ocultar-editor'],
            slot=self.visibilidad_contenedor_principal)
        self.accionMostrarOcultarEditor.setCheckable(True)
        # Mostrar/ocultar consola
        self.accionMostrarOcultarInput = crear_accion(self,
            "Mostrar/ocultar consola", atajo=_ATAJO['ocultar-input'],
            slot=self.visibilidad_contenedor_secundario)
        # Acercar
        self.accionAcercar = crear_accion(self, "Acercar",
            icono=_ICONO['acercar'], atajo=_ATAJO['zoom-mas'],
            slot=self._acercar)
        # Alejar
        self.accionAlejar = crear_accion(self, "Alejar",
            icono=_ICONO['alejar'], atajo=_ATAJO['zoom-menos'],
            slot=self._alejar)

        # Agregar acciones al menú #
        menu_ver.addAction(self.accionFullScreen)
        menu_ver.addAction(self.accionMostrarLateral)
        menu_ver.addAction(self.accionMostrarOcultarToolbar)
        menu_ver.addAction(self.accionMostrarOcultarEditor)
        menu_ver.addAction(self.accionMostrarOcultarInput)
        menu_ver.addSeparator()
        menu_ver.addAction(self.accionAcercar)
        menu_ver.addAction(self.accionAlejar)

        self.accionFullScreen.setChecked(False)
        self.accionMostrarLateral.setChecked(True)
        self.accionMostrarOcultarToolbar.setChecked(True)
        self.accionMostrarOcultarEditor.setChecked(True)
        self.accionMostrarOcultarInput.setChecked(False)

        self.items_toolbar = {
            "acercar": self.accionAcercar,
            "alejar": self.accionAlejar
            }

    def pantalla_completa(self):
        """ Muestra en pantalla completa. """

        if self.ide.isFullScreen():
            self.ide.showMaximized()
        else:
            self.ide.showFullScreen()

    def ocultar_mostrar_toolbars(self):
        """ Muestra/oculta las toolbars """

        if self.ide.toolbar.isVisible():
            self.ide.toolbar.hide()
            #self.ide.toolbar_.hide()
        else:
            self.ide.toolbar.show()
            #self.ide.toolbar.show()

    def ocultar_mostrar_navegador(self):
        if self.ide.explorador.isVisible():
            self.ide.explorador.hide()
        else:
            self.ide.explorador.show()

    def visibilidad_contenedor_principal(self):
        self.ide.widget_Central.visibilidad_contenedor_principal()
        self.ide._menu_ver.accionMostrarOcultarEditor.setChecked(
            self.ide.widget_Central.contenedor_principal.isVisible())

    def visibilidad_contenedor_secundario(self):
        self.ide.widget_Central.mostrar_ocultar_widget_bottom()
        self.ide._menu_ver.accionMostrarOcultarInput.setChecked(
            self.ide.widget_Central.contenedor_bottom.isVisible())

    def modo_dev(self):
        """ Oculta/Muestra todo excepto el editor. """

        if self.ide.menuBar().isVisible():
            self.ide.toolbar.hide()
            #self.ide.toolbar_.hide()
            self.ide.menuBar().hide()
            self.ide.contenedor_secundario.hide()
        else:
            self.ide.toolbar.show()
            #self.ide.toolbar_.show()
            self.ide.menuBar().show()
        self.ide._menu_ver.accionMostrarOcultarTodo.setChecked(
            self.ide.menuBar().isVisible())
        self.ide._menu_ver.accionMostrarOcultar_input.setChecked(
            self.ide.widget_Central.contenedor_bottom.isVisible())
        self.ide._menu_ver.accionMostrarOcultarEditor.setChecked(
            self.ide.widget_Central.contenedor_principal.isVisible())
        self.ide._menu_ver.accionMostrarOcultarToolbar.setChecked(
            self.ide.toolbar.isVisible())
        #self.ide._menu_ver.accionMostrarOcultarToolbar.setChecked(
            #self.ide.toolbar_.isVisible())

    def _acercar(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            editor.acercar()

    def _alejar(self):
        editor = self.ide.contenedor_principal.devolver_editor_actual()
        if editor:
            editor.alejar()
