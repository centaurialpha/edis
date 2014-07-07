#-*- coding: utf-8 -*-

# <Contenedor Principal.>
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

import os

from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog
#from PyQt4.QtGui import QMessageBox
#from PyQt4.QtGui import QApplication

from PyQt4.QtCore import SIGNAL

from edis_c import recursos
from edis_c.interfaz import tab_widget
from edis_c.interfaz import pagina_inicio
from edis_c.interfaz.editor import editor
from edis_c.nucleo import manejador_de_archivo

__instanciaContenedorMain = None


# Singleton
def ContenedorMain(*args, **kw):
    global __instanciaContenedorMain
    if __instanciaContenedorMain is None:
        __instanciaContenedorMain = __ContenedorMain(*args, **kw)
    return __instanciaContenedorMain


class __ContenedorMain(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)

        self.parent = parent
        self.tab_principal = tab_widget.TabCentral(self)
        self.setAcceptDrops(True)
        self.addWidget(self.tab_principal)
        self.setSizes([1, 1])
        self.setFixedSize(0, 500)
        self.tab_actual = self.tab_principal

    #    self.connect(self.tab_principal, SIGNAL("currentChanged(int)"),
     #       self.tab_actual_cambiado)
        self.connect(self.tab_principal, SIGNAL("saveActualEditor()"),
            self.guardar_archivo)
        self.connect(self.tab_principal, SIGNAL("currentChanged(int)"),
            self.tab_actual_cambiado)

    def agregar_editor(self, nombre_archivo="", tabIndex=None):
        editorWidget = editor.crear_editor(nombre_archivo=nombre_archivo)

        if not nombre_archivo:
            nombre_tab = "Nuevo archivo"
        else:
            nombre_tab = manejador_de_archivo._nombreBase(nombre_archivo)

        self.agregar_tab(editorWidget, nombre_tab, tabIndex=tabIndex)

        self.connect(editorWidget, SIGNAL("modificationChanged(bool)"),
            self.editor_es_modificado)
        self.connect(editorWidget, SIGNAL("fileSaved(QPlainTextEdit)"),
            self.editor_es_guardado)
        self.connect(editorWidget, SIGNAL("openDropFile(QString)"),
            self.abrir_archivo)
        self.emit(SIGNAL("fileOpened(QString)"), nombre_archivo)
        self.connect(editorWidget, SIGNAL("cursorPositionChange(int, int)"),
            self._posicion_del_cursor)

        return editorWidget

    def _editor_keyPressEvent(self, evento):
        self.emit(SIGNAL("editorKeyPressEvent(QEvent)"), evento)

    def editor_es_modificado(self, v=True):
        self.tab_actual.tab_es_modificado(v)

    def editor_es_guardado(self, editorW=None):
        self.tab_actual.tab_guardado(editorW)
        #self.emit(SIGNAL("updateLocator(QString)"), editorW.ID)

    def check_tabs_sin_guardar(self):
        return self.tab_principal.check_tabs_sin_guardar()

    def devolver_archivos_no_guardados(self):
        return self.tab_principal.devolver_archivos_no_guardados()

    def agregar_tab(self, widget, nombre_tab, tabIndex=None, nAbierta=True):
        return self.tab_actual.agregar_tab(widget, nombre_tab, index=tabIndex)

    def devolver_widget_actual(self):
        return self.tab_actual.currentWidget()

    def devolver_editor_actual(self):
        e = self.tab_actual.currentWidget()
        if isinstance(e, editor.Editor):
            return e
        else:
            return None

    def deshacer(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.undo()

    def rehacer(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.redo()

    def cortar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.cut()

    def copiar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.copy()

    def pegar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.paste()

    def seleccionar_todo(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.selectAll()

    def borrar(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.clear()

    def indentar_mas(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.indentar_mas()

    def indentar_menos(self):
        editorW = self.devolver_editor_actual()
        if editorW:
            editorW.indentar_menos()

    def convertir_a_mayusculas(self):
        editor = self.devolver_editor_actual()
        if editor:
            editor.convertir_a_mayusculas()

    def convertir_a_minusculas(self):
        editor = self.devolver_editor_actual()
        if editor:
            editor.convertir_a_minusculas()

    def actualizar_margen_editor(self):
        for i in range(self.tab_principal.count()):
            widget = self.tab_principal.widget(i)
            #if type(widget) is editor.Editor:
            if isinstance(widget, editor.Editor):
                widget.actualizar_margen_linea()

    def mostrar_pagina_de_inicio(self):
        pag = pagina_inicio.PaginaDeInicio(parent=self)
        self.agregar_tab(pag, self.trUtf8('Página de inicio'))

    def setFocus(self):
        w = self.devolver_widget_actual()
        if w:
            w.setFocus()

    def _posicion_del_cursor(self, linea, columna):
        self.emit(SIGNAL("cursorPositionChange(int, int)"), linea, columna)

    def cerrar_tab(self):
        """ Se llama al método removeTab de QTabWidget. """

        self.tab_actual.cerrar_tab()

    def cerrar_todo(self):
        self.tab_actual.cerrar_todo()

    def cerrar_excepto_actual(self):
        self.tab_actual.cerrar_excepto_actual()

    def actual_widget(self):
        return self.tab_actual.currentWidget()

    def tab_actual_cambiado(self, indice):
        if self.tab_actual.widget(indice):
            self.emit(SIGNAL("currentTabChanged(QString)"),
                self.tab_actual.widget(indice)._id)

    def cambiar_nombre_de_tab(self, aidi, nuevoId):
        indice_tab = self.tab_principal.esta_abierto(aidi)
        if indice_tab is not False:
            w = self.tab_principal.w(indice_tab)
            TAB = self.tab_principal

        nombre_de_tab = manejador_de_archivo._nombreBase(nuevoId)
        TAB.cambiar_nombre_de_tab(indice_tab, nombre_de_tab)
        w.ID = nuevoId

    def abrir_archivo(self, nombre='', tabIndex=None):
        extension = recursos.EXTENSIONES  # Filtro

        nombre = str(nombre)

        if not nombre:
            direc = os.path.expanduser("~")

            nombres = list(QFileDialog.getOpenFileNames(self,
            self.trUtf8("Abrir archivo"), direc, extension))

        else:
            nombres = [nombre]

        for nombre in nombres:
            nombre = str(nombre)

            self.tab_actual.no_esta_abierto = False
            #contenido = self.leer_contenido_archivo(nombre)
            contenido = manejador_de_archivo.leer_contenido_de_archivo(
                nombre)
            editorW = self.agregar_editor(nombre, tabIndex=tabIndex)
            editorW.setPlainText(contenido.decode('utf-8'))
            editorW.ID = nombre
            # Test not empty
            editorW.nuevo_archivo = False
            self.emit(SIGNAL("currentTabChanged(QString)"), nombre)

        self.tab_actual.no_esta_abierto = True

    def guardar_archivo(self, editorW=None):
        if not editorW:
            editorW = self.devolver_editor_actual()
            if not editorW:
                return False

        try:
            editorW.guardado_actualmente = True

            if editorW.nuevo_archivo or \
            not manejador_de_archivo.permiso_de_escritura(editorW.ID):
                return self.guardar_archivo_como()

            nombre = editorW.ID
            self.emit(SIGNAL("beforeFileSaved(QString)"), nombre)
            contenido = editorW.devolver_texto()
            manejador_de_archivo.escribir_archivo(nombre, contenido)
            editorW.ID = nombre

            self.emit(SIGNAL("fileSaved(QString)"), self.tr(
                "Guardado: %1").arg(nombre))

            editorW._guardado()

            return editorW.ID
        except:
            editorW.guardado_actualmente = False
        return False

    def guardar_archivo_como(self):
        editorW = self.devolver_editor_actual()
        if not editorW:
            return False

        direc = os.path.expanduser("~")

        try:
            editorW.guardado_actualmente = True
            nombre = str(QFileDialog.getSaveFileName(
                self.parent, self.tr("Guardar"), direc, '(*.c);;(*.*)'))
            if not nombre:
                return False

            nombre = manejador_de_archivo.escribir_archivo(
                nombre, editorW.devolver_texto())

            self.tab_actual.setTabText(self.tab_actual.currentIndex(),
                manejador_de_archivo._nombreBase(nombre))
            editorW.ID = nombre

            # Señal de guardado para la barra de estado
            self.emit(SIGNAL("fileSaved(QString)"),
                self.tr("Guardado: %1").arg(nombre))
            editorW._guardado()

            return editorW.ID

        except:
            #pass
            editorW.guardado_actualmente = False
            self.tab_actual.setTabText(self.tab_actual.currentIndex(),
                self.trUtf8("Nuevo archivo"))
        return False

    def guardar_todo(self):

        for i in range(self.tab_principal.count()):
            editorW = self.tab_principal.widget(i)

            if isinstance(editorW, editor.Editor):
                self.guardar_archivo(editorW)

    def esta_abierto(self, nombre):
        return self.tab_principal.esta_abierto(nombre) is not False