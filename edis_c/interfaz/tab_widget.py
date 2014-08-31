#-*- coding: utf-8 -*-

# <Widget de pestañas.>
# This file is part of EDIS-C.

# Copyright (C) <2014>  <Gabriel Acosta>

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
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QAction
#from PyQt4.QtGui import QSizePolicy
#from PyQt4.QtGui import QSpacerItem

# Módulos QtCore
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

# Módulos EDIS
from edis_c import recursos
from edis_c.interfaz.editor import editor


class TabCentral(QTabWidget):

    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)
        self.parent = parent
        self.no_esta_abierto = True
        self.boton = BotonTab()
        self.setCornerWidget(self.boton, Qt.TopLeftCorner)
        self.connect(self, SIGNAL("tabCloseRequested(int)"),
            self.removeTab)
        self.boton.accionCerrar.triggered.connect(self.cerrar_tab)
        self.boton.accionCerrarTodo.triggered.connect(self.cerrar_todo)
        self.boton.accionCerrarExcepto.triggered.connect(
            self.cerrar_excepto_actual)

    def agregar_tab(self, widget, icono, titulo):
        """ Agrega una pestaña
        @widget: tipo de widget (generalmente se obtiene un QPlainTextEdit)
        @icono: ícono para la pestaña.
        @titulo: texto de la pestaña.
        """
        tab = self.addTab(widget, QIcon(icono), titulo)
        self.setCurrentIndex(tab)
        widget.setFocus()
        return tab

    def cerrar_tab(self):
        """ Cierra la pestaña actual. """

        self.removeTab(self.currentIndex())

    def cerrar_todo(self):
        """ Cierra todas las pestañas. """

        for tab in range(self.count()):
            self.removeTab(0)

    def cerrar_excepto_actual(self):
        """ Cierrar todas las pestañas excepto la pestaña actual.
        """

        self.tabBar().moveTab(self.currentIndex(), 0)
        for tab in range(self.count()):
            if self.count() > 1:
                self.removeTab(1)

    def tab_es_modificado(self, v):
        """ @v: valor booleano. """

        e = self.currentWidget()
        if isinstance(e, editor.Editor) and self.no_esta_abierto and v:
            e.texto_modificado = True
            self.tabBar().setTabTextColor(self.currentIndex(),
                QColor(Qt.red))

    def tab_guardado(self, e):
        """ @e: valor booleano. """
        indice = self.indexOf(e)
        self.tabBar().setTabTextColor(indice, QColor(70, 70, 70))

    def check_tabs_sin_guardar(self):
        """ Devuelve Verdadero si hay algún editor que fué modificado
        y no se han guardado los cambios """

        valor = False
        for i in range(self.count()):
            if isinstance(self.widget(i), editor.Editor):
                valor = valor or self.widget(i).texto_modificado

        return valor

    def devolver_documentos_para_reabrir(self):
        archivos = []
        for i in range(self.count()):
            if isinstance(self.widget(i), editor.Editor) \
            and self.widget(i)._id != '':
                archivos.append([self.widget(i)._id,
                    self.widget(i).devolver_posicion_del_cursor()])
        return archivos

    def devolver_archivos_sin_guardar(self):
        """ Devuelve una lista de todos los archivos que han sido modificados
        y no se han guardado."""

        archivos = []

        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, editor.Editor) and w.texto_modificado:
                archivos.append(str(self.tabText(i)))

        return archivos

    def focusInEvent(self, e):
        QTabWidget.focusInEvent(self, e)
        self.emit(SIGNAL("changeActualTab(QTabWidget)"), self)

        eW = self.currentWidget()
        if not eW:
            return
        if eW.nuevo_archivo:
            return

    def actualizar_widget_actual(self):
        if self.currentWidget() is not None:
            self.currentWidget().setFocus()
        else:
            self.emit(SIGNAL("allTabsClosed()"))

    def removeTab(self, indice):
        """ Reimplementación del método removeTab de QTabWidget. """

        if indice != -1:
            self.setCurrentIndex(indice)
            w = self.currentWidget()

            SI = QMessageBox.Yes
            NO = QMessageBox.No
            CANCELAR = QMessageBox.Cancel

            if isinstance(w, editor.Editor):
                respuesta = NO
                if w.texto_modificado:
                    nombre = self.tabBar().tabText(self.currentIndex())
                    respuesta = QMessageBox.question(self,
                        (str(self.trUtf8('El archivo **%s no esta guardado')) %
                        str(nombre)), self.trUtf8("¿Guardar antes de cerrar?"),
                            SI | NO | CANCELAR)

                if respuesta == SI:
                    self.emit(SIGNAL("saveActualEditor()"))
                    if w.texto_modificado:
                        return
                elif respuesta == CANCELAR:
                    return

            super(TabCentral, self).removeTab(indice)
            if self.currentWidget() is not None:
                self.currentWidget().setFocus()
            else:
                self.emit(SIGNAL("allTabsClosed()"))
            del w
            self.actualizar_widget_actual()


class BotonTab(QToolButton):
    """ Botón personalizado colocado a la izquierda del QTabWidget. """

    def __init__(self):
        super(BotonTab, self).__init__()
        self.setAutoRaise(True)
        self.setIcon(QIcon(recursos.ICONOS['tab']))
        self.setPopupMode(2)
        self.crear_menu()

    def crear_menu(self):
        """ Menú """

        menu = QMenu(self)
        self.accionCrear = QAction(self.trUtf8("Nueva pestaña"), self)
        self.accionCerrar = QAction(self.trUtf8("Cerrar"), self)
        self.accionCerrarTodo = QAction(self.trUtf8("Cerrar todo"), self)
        self.accionCerrarExcepto = QAction(
            self.trUtf8("Cerrar los demás"), self)
        menu.addAction(self.accionCrear)
        menu.addSeparator()
        menu.addAction(self.accionCerrar)
        menu.addAction(self.accionCerrarTodo)
        menu.addAction(self.accionCerrarExcepto)
        self.setMenu(menu)