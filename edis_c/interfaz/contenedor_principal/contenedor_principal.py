#-*- coding: utf-8 -*-

# <Contenedor Principal.>
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

# Módulos Python
import os
import re

# Módulos QtGui
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QIcon

# Módulos QtCore
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QFile
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

# Módulos EDIS
from edis_c.nucleo import manejador_de_archivo
from edis_c import recursos
from edis_c.interfaz import tab_widget
from edis_c.interfaz.widgets import pagina_de_bienvenida
from edis_c.interfaz.editor import editor
from edis_c.interfaz.editor import highlighter_
from edis_c.interfaz.editor import acciones_

__instanciaContenedorMain = None


# Singleton
def ContenedorMain(*args, **kw):
    global __instanciaContenedorMain
    if __instanciaContenedorMain is None:
        __instanciaContenedorMain = __ContenedorMain(*args, **kw)
    return __instanciaContenedorMain


class __ContenedorMain(QSplitter):
    """ Splitter principal que contiene el editor. """

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)

        self.parent = parent
        self.tab_principal = tab_widget.TabCentral(self)
        self.setAcceptDrops(True)
        self.addWidget(self.tab_principal)
        self.setSizes([1, 1])
        self.setFixedSize(0, 450)
        self.tab_actual = self.tab_principal
        highlighter_.re_estilo(recursos.NUEVO_TEMA)
    #    self.connect(self.tab_principal, SIGNAL("currentChanged(int)"),
     #       self.tab_actual_cambiado)
        self.connect(self.tab_principal, SIGNAL("saveActualEditor()"),
            self.guardar_archivo)
        self.connect(self.tab_principal, SIGNAL("currentChanged(int)"),
            self.tab_actual_cambiado)
        self.tab_principal.boton.accionCrear.triggered.connect(
            lambda: self.agregar_editor(''))

        tecla = Qt.Key_1
        for i in range(10):
            atajo = TabAtajos(QKeySequence(Qt.ALT + tecla), self.parent, i)
            tecla += 1
            atajo.activated.connect(self.cambiar_indice_de_tab)

    def agregar_editor(self, nombre_archivo=""):
        """ Agrega un QPlainTextEdit
            @nombre_archivo: texto QString para el nombre del documento.
            por defecto False.
        """

        editorWidget = editor.crear_editor(nombre_archivo=nombre_archivo)
        if not nombre_archivo:
            nombre_tab = "Nuevo archivo"
            icono = False
        else:
            nombre_tab = manejador_de_archivo._nombreBase(nombre_archivo)
            ext = nombre_tab.strip('.')[-1]
            if ext == 'c':
                icono = recursos.ICONOS['main']
            elif ext == 'h':
                icono = recursos.ICONOS['cabecera']
            else:
                icono = False

        indice = self.agregar_tab(editorWidget, icono, nombre_tab)
        self.tab_actual.setTabToolTip(indice,
            QDir.toNativeSeparators(nombre_archivo))
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

    def check_tabs_sin_guardar(self):
        return self.tab_principal.check_tabs_sin_guardar()

    def devolver_archivos_sin_guardar(self):
        """ Retorna una lista con archivos sin guardar. """

        return self.tab_principal.devolver_archivos_sin_guardar()

    def agregar_tab(self, widget, icono, nombre_tab, nAbierta=True):
        """ Se llama al método agregar_tab de la clase TabCentral
        retorna QTabWidget.
        """

        return self.tab_actual.agregar_tab(widget, icono, nombre_tab)

    def devolver_widget_actual(self):
        """ Retorna QTabWidget actual. """

        return self.tab_actual.currentWidget()

    def devolver_editor_actual(self):
        """ Si el widget es una instancia de QPlainTextEdit se lo retorna,
        de lo contrario se retorna None.
        """

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

    def actualizar_margen_editor(self):
        for i in range(self.tab_principal.count()):
            widget = self.tab_principal.widget(i)
            #if type(widget) is editor.Editor:
            if isinstance(widget, editor.Editor):
                widget.actualizar_margen_linea()

    def mostrar_pagina_de_bienvenida(self):
        pag = pagina_de_bienvenida.PaginaDeBienvenida(parent=self)
        self.agregar_tab(pag, False, self.trUtf8('EDIS-C'))
        self.connect(pag, SIGNAL("nuevoArchivo()"),
            lambda: self.emit(SIGNAL("nuevoArchivo()")))
        self.connect(pag, SIGNAL("abrirArchivo()"),
            lambda: self.emit(SIGNAL("abrirArchivo()")))

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
        w.iD = nuevoId

    def cambiar_indice_de_tab(self):
        Weditor = self.parent.contenedor_principal.devolver_editor_actual()
        if Weditor is not None and Weditor.hasFocus():
            contenedor = self.parent.contenedor_principal.tab_actual
        else:
            return None
        obj = self.sender()
        if obj.indice < contenedor.count():
            contenedor.setCurrentIndex(obj.indice)

    def abrir_archivo(self, nombre=''):
        extension = recursos.EXTENSIONES  # Filtro

        nombre = unicode(nombre)

        if not nombre:

            direc = os.path.expanduser("~")
            Weditor = self.devolver_editor_actual()
            # Para recordar la última carpeta
            if Weditor is not None and Weditor._id:
                direc = manejador_de_archivo.devolver_carpeta(Weditor._id)
            nombres = list(QFileDialog.getOpenFileNames(self,
            self.trUtf8("Abrir archivo"), direc, extension))

        else:
            nombres = [nombre]
        if not nombres:
            return

        for nombre in nombres:
            nombre = unicode(nombre)
            self.tab_actual.no_esta_abierto = False
            #contenido = self.leer_contenido_archivo(nombre)
            contenido = manejador_de_archivo.leer_contenido_de_archivo(
                nombre)
            editorW = self.agregar_editor(nombre)
            editorW.setPlainText(contenido.decode('utf-8'))
            editorW.iD = nombre

            # Reemplaza tabulaciones por espacios en blanco
            editorW.tabulaciones_por_espacios_en_blanco()
            editorW.nuevo_archivo = False
        self.emit(SIGNAL("currentTabChanged(QString)"), nombre)
        self.tab_actual.no_esta_abierto = True

    def devolver_documentos_abiertos(self):
        return [self.tab_principal.devolver_documentos_para_reabrir(), []]

    def guardar_archivo(self, editorW=None):
        if not editorW:
            editorW = self.devolver_editor_actual()
            if not editorW:
                return False

        try:
            editorW.guardado_actualmente = True

            if editorW.nuevo_archivo or \
            not manejador_de_archivo.permiso_de_escritura(editorW._id):
                return self.guardar_archivo_como()

            nombre = editorW._id
            carpeta_de_archivo = manejador_de_archivo.devolver_carpeta(nombre)
            self.emit(SIGNAL("beforeFileSaved(QString)"), nombre)
            acciones_.quitar_espacios_en_blanco(editorW)
            contenido = editorW.devolver_texto()
            manejador_de_archivo.escribir_archivo(nombre, contenido)
            editorW.iD = nombre

            self.emit(SIGNAL("fileSaved(QString)"), self.tr(
                "Guardado: %0 en %1").arg((nombre).split('/')[-1],
                carpeta_de_archivo))

            editorW._guardado()

            return editorW._id
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

            acciones_.quitar_espacios_en_blanco(editorW)
            nombre = manejador_de_archivo.escribir_archivo(
                nombre, editorW.devolver_texto())
            ext = manejador_de_archivo._nombreBase(nombre)[-1]
            if ext == 'c':
                icono = recursos.ICONOS['main']
            else:
                icono = recursos.ICONOS['cabecera']
            self.tab_actual.setTabText(self.tab_actual.currentIndex(),
                manejador_de_archivo._nombreBase(nombre))
            self.tab_actual.setTabIcon(self.tab_actual.currentIndex(),
                QIcon(icono))
            editorW.iD = nombre

            # Señal de guardado para la barra de estado
            self.emit(SIGNAL("fileSaved(QString)"),
                self.tr("Guardado: %1").arg(nombre))
            editorW._guardado()

            return editorW._id

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

    def resetear_flags_editor(self):
        for i in range(self.tab_principal.count()):
            widget = self.tab_principal.widget(i)
            if isinstance(widget, editor.Editor):
                widget.set_flags()

    def estadisticas(self):
        editor = self.devolver_editor_actual()
        if editor:
            # ruta del archivo
            tex = editor._id
            # se obtiene el nombre con la extensión
            #FIXME: no luce bien... pero funciona ;)
            tex = tex.split('/')[-1]  # En Linux
            tex = tex.split('\\')[-1]  # En Windows

            # Tamaño en kb
            #FIXME: ¿ bien ?
            lonB = (float(QFile(editor._id).size() + 1023.0) / 1024.0)

            cantidad_lineas = editor.devolver_cantidad_de_lineas()
            # Espacios en blanco y comentarios
            espacios_com = re.findall('(^\n)|(^(\s+)?//)|(^( +)?($|\n))',
                unicode(editor.devolver_texto()), re.M)
            cantidad_esp = len(espacios_com)

            dialogo = QDialog(self)
            dialogo.setWindowTitle(self.trUtf8("Estadísticas del documento"))
            layoutV = QVBoxLayout(dialogo)
            layoutV.setContentsMargins(10, 15, 10, 10)
            layoutV.setSpacing(10)

            label = QLabel(self.trUtf8("%1").arg(tex))
            label.setStyleSheet("font-weight: bold; font-size: 24px;")
            layoutV.addWidget(label)
            grilla = QGridLayout()
            grilla.addWidget(QLabel(" "), 1, 0)
            grilla.addWidget(QLabel(self.trUtf8(
                "Líneas de código")), 2, 1, Qt.AlignLeft)
            grilla.addWidget(QLabel(self.trUtf8(
                "%1").arg(cantidad_lineas - cantidad_esp)),
                2, 4, Qt.AlignRight)
            grilla.addWidget(QLabel(self.trUtf8(
                "Espacios en blanco y comentarios")), 3, 1, Qt.AlignLeft)
            grilla.addWidget(QLabel(self.trUtf8(
                "%1").arg(cantidad_esp)), 3, 4, Qt.AlignRight)
            grilla.addWidget(QLabel(self.trUtf8(
                "Tamaño (kb)")), 4, 1, Qt.AlignLeft)
            grilla.addWidget(QLabel(self.trUtf8(
                "%1").arg(lonB)), 4, 4, alignment=Qt.AlignRight)
            grilla.addWidget(QLabel(self.trUtf8(
                "Total de líneas")), 5, 1, Qt.AlignLeft)
            grilla.addWidget(QLabel(self.trUtf8(
                "%1").arg(cantidad_lineas)), 5, 4, Qt.AlignRight)
            boton_aceptar = QPushButton(self.trUtf8("Aceptar"))
            grilla.addWidget(boton_aceptar, 6, 4)
            layoutV.addLayout(grilla)

            boton_aceptar.clicked.connect(dialogo.close)

            dialogo.show()


class TabAtajos(QShortcut):

    def __init__(self, tecla, parent, indice):
        super(TabAtajos, self).__init__(tecla, parent)
        self.indice = indice