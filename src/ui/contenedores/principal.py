# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.Qsci import QsciPrinter

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QPrintPreviewDialog,
    QTextDocument,
    QInputDialog
    )

from PyQt4.QtCore import (
    SIGNAL,
    QFileInfo,
    pyqtSignal,
    )

from src.helpers import (
    manejador_de_archivo,
    )
from src.ui.editor import (
    editor,
    stack
    )
from src.ui.edis_main import EDIS
from src.ui.widgets import popup_busqueda
from src.ui.contenedores import selector
from src.ui.dialogos import (
    dialogo_propiedades,
    dialogo_log,
    dialogo_proyecto,
    dialogo_reemplazo
    )


class EditorContainer(QWidget):

    archivo_cambiado = pyqtSignal(['QString'])
    archivo_abierto = pyqtSignal(['QString'])
    posicion_cursor = pyqtSignal(int, int, int)
    archivo_modificado = pyqtSignal(bool)
    actualizar_simbolos = pyqtSignal(['QString'], name="actualizarSimbolos")
    archivo_cerrado = pyqtSignal(int)
    cambiar_item = pyqtSignal(int)

    def __init__(self, edis=None):
        QWidget.__init__(self, edis)
        self.setAcceptDrops(True)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.stack = stack.StackWidget(self)
        vbox.addWidget(self.stack)

        self.instalar_signals()
        EDIS.cargar_componente("principal", self)

    def instalar_signals(self):
        self.connect(self.stack, SIGNAL("Guardar_Editor_Actual()"),
                    self.guardar_archivo)
        self.connect(self.stack, SIGNAL("archivo_modificado(bool)"),
                    self._archivo_modificado)
        self.connect(self.stack, SIGNAL("archivo_cerrado(int)"),
                    self._archivo_cerrado)
        self.connect(self.stack, SIGNAL("archivo_reciente(QStringList)"),
                    self.actualizar_recientes)

    def actualizar_recientes(self, recientes):
        edis = EDIS.componente('edis')
        menu = edis.accion('Abrir reciente')
        self.connect(menu, SIGNAL("triggered(QAction*)"), self._abrir_reciente)
        menu.clear()
        for archivo in recientes:
            menu.addAction(archivo)

    def _abrir_reciente(self, accion):
        self.abrir_archivo(accion.text())

    def _archivo_cerrado(self, indice):
        self.archivo_cerrado.emit(indice)
        self.cambiar_widget(indice)

    def _archivo_modificado(self, valor):
        self.archivo_modificado.emit(valor)

    def __archivo_guardado(self, weditor):
        self.actualizar_simbolos.emit(weditor.nombre)
        self.archivo_modificado.emit(False)

    def cambiar_widget(self, indice):
        self.stack.cambiar_widget(indice)
        weditor = self.devolver_editor()
        if weditor is not None:
            self.archivo_cambiado.emit(weditor.nombre)
            self.cambiar_item.emit(indice)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        weditor = editor.crear_editor(nombre)
        self.agregar_widget(weditor)
        weditor.modificationChanged[bool].connect(self.stack.editor_modificado)
        weditor.cursorPositionChanged[int, int].connect(self.actualizar_cursor)
        weditor.archivo_guardado.connect(self.__archivo_guardado)
        weditor.dropSignal.connect(self._drop_editor)
        weditor.setFocus()
        return weditor

    def abrir_archivo(self, nombre=""):
        filtro = "Archivos C/C++(*.cpp *.c);;ASM(*.s);;HEADERS(*.h);;(*.*)"
        if not nombre:
            carpeta = os.path.expanduser("~")
            editor_widget = self.widget_actual()
            if editor_widget and editor_widget.nombre:
                carpeta = self.__ultima_carpeta_visitada(editor_widget.nombre)
            archivos = QFileDialog.getOpenFileNames(self,
                            self.trUtf8("Abrir archivo"), carpeta, filtro)
        else:
            archivos = [nombre]
        for archivo in archivos:
            if not self.__archivo_abierto(archivo):
                self.stack.no_esta_abierto = False
                contenido = manejador_de_archivo.leer_contenido_de_archivo(
                            archivo)
                nuevo_editor = self.agregar_editor(archivo)
                nuevo_editor.texto = contenido
                nuevo_editor.nombre = archivo
                self.archivo_cambiado.emit(archivo)
                self.archivo_abierto.emit(archivo)

        self.stack.no_esta_abierto = True

    def __ultima_carpeta_visitada(self, path):
        """ Devuelve la última carpeta a la que se accedió """

        return QFileInfo(path).absolutePath()

    def __archivo_abierto(self, archivo):
        """
        Retorna True si un archivo ya esta abierto,
        False en caso contrario

        """

        editores = self.stack.editores
        for editor_widget in editores:
            if editor_widget.nombre == archivo:
                return True
        return False

    def agregar_widget(self, widget):
        """ Agrega @widget al stacked """

        self.stack.agregar_widget(widget)

    def eliminar_widget(self, widget):
        """ Elimina el @widget del stacked """

        self.stack.removeWidget(widget)

    def widget_actual(self):
        """ Widget actual """

        return self.stack.widget_actual

    def indice_actual(self):
        return self.stack.indice_actual

    def devolver_editor(self):
        """ Devuelve el Editor si el widget actual es una instancia de él,
        de lo contrario devuelve None. """

        widget = self.widget_actual()
        if isinstance(widget, editor.Editor):
            return widget
        return None

    def cerrar_archivo(self):
        self.stack.cerrar()

    def cerrar_todo(self):
        self.stack.cerrar_todo()

    def cerrar_demas(self):
        self.stack.cerrar_demas()

    def selector(self):
        if self.devolver_editor() is not None:
            selector_ = selector.Selector(self)
            selector_.show()

    def guardar_archivo(self, weditor=None):
        #FIXME: Controlar con try-except
        if not weditor:
            weditor = self.devolver_editor()
            if not weditor:
                return False

        if weditor.es_nuevo:
            return self.guardar_archivo_como(weditor)
        nombre_archivo = weditor.nombre
        codigo_fuente = weditor.texto
        manejador_de_archivo.escribir_archivo(nombre_archivo, codigo_fuente)
        weditor.nombre = nombre_archivo
        weditor.guardado()

    def guardar_archivo_como(self, weditor):
        #FIXME: Controlar con try-except
        carpeta = os.path.expanduser("~")
        nombre_archivo = QFileDialog.getSaveFileName(self,
                self.trUtf8("Guardar archivo"), carpeta)
        if not nombre_archivo:
            return False
        nombre_archivo = manejador_de_archivo.escribir_archivo(nombre_archivo,
                weditor.texto)
        weditor.nombre = nombre_archivo
        self.archivo_cambiado.emit(nombre_archivo)
        weditor.guardado()

    def guardar_todo(self):
        for editor in self.stack.editores:
            self.guardar_archivo(editor)

    def guardar_seleccionado(self, archivo):
        for i in range(self.stack.contar):
            if self.stack.editor(i).nombre == archivo:
                self.guardar_archivo(self.stack.editor(i))

    def archivos_sin_guardar(self):
        return self.stack.archivos_sin_guardar()

    def check_archivos_sin_guardar(self):
        return self.stack.check_archivos_sin_guardar()

    def busqueda(self):
        #FIXME:
        dialogo = popup_busqueda.PopupBusqueda(self.devolver_editor())
        dialogo.show()

    def reemplazar(self):
        dialogo = dialogo_reemplazo.DialogoReemplazo(self)
        dialogo.show()

    def deshacer(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.deshacer()

    def rehacer(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.rehacer()

    def cortar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.cortar()

    def copiar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.copiar()

    def pegar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.pegar()

    def mostrar_tabs_espacios_blancos(self):
        #FIXME:
        #accion = EDIS.accion("Mostrar tabs y espacios en blanco")
        #configuraciones.MOSTRAR_TABS = accion.isChecked()
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.actualizar()

    def mostrar_guias(self):
        #FIXME:
        #accion = EDIS.accion("Mostrar guías")
        #configuraciones.GUIA_INDENTACION = accion.isChecked()
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.actualizar()

    def acercar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_in()

    def seleccionar_todo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.seleccionar()

    def alejar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_out()

    def archivos_abiertos(self):
        return self.stack.archivos_abiertos()

    def propiedades_de_archivo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            dialogo = dialogo_propiedades.FileProperty(weditor, self)
            dialogo.show()

    def archivo_log(self):
        dialogo = dialogo_log.DialogoLog(self)
        dialogo.show()

    def actualizar_cursor(self, linea, columna):
        weditor = self.devolver_editor()
        lineas = weditor.lineas
        self.posicion_cursor.emit(linea + 1, columna + 1, lineas)

    def compilar_codigo_fuente(self):
        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        weditor = self.devolver_editor()
        if weditor is not None:
            self.guardar_archivo(weditor)
            output.compilar(weditor.nombre)

    def ejecutar_programa(self):
        """ Ejecuta el programa objeto """

        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        output.ejecutar()

    def compilar_ejecutar(self):
        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        weditor = self.devolver_editor()
        if weditor is not None:
            self.guardar_archivo(weditor)
            output.compilar_ejecutar(weditor.nombre)

    def limpiar_construccion(self):
        edis = EDIS.componente("edis")
        output = edis.contenedor_output
        output.limpiar()

    def terminar_programa(self):
        edis = EDIS.componente("edis")
        edis.contenedor_output.terminar_programa()

    def imprimir_documento(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            # Extensión
            ext = weditor.nombre.split('.')[-1]
            # Se reemplaza la extensión por 'pdf'
            nombre = weditor.nombre.replace(ext, 'pdf')
            documento = QTextDocument(weditor.texto)
            printer = QsciPrinter()
            printer.setPageSize(QsciPrinter.A4)
            printer.setOutputFileName(nombre)
            printer.setDocName(nombre)

            dialogo = QPrintPreviewDialog(printer)
            dialogo.paintRequested.connect(documento.print_)
            dialogo.exec_()

    def comentar_documento(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.comentar()

    def descomentar_documento(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.descomentar()

    def indentar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.indentar()

    def remover_indentacion(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.quitar_indentacion()

    def convertir_a_titulo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.a_titulo()

    def duplicar_linea(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.duplicar_linea()

    def eliminar_linea(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.eliminar_linea()

    def mover_linea_abajo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.mover_linea_abajo()

    def mover_linea_arriba(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.mover_linea_arriba()

    def ir_a_linea(self, linea):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.setCursorPosition(linea, 0)

    def plegar_desplegar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.foldAll()

    def ir_a_linea_dialogo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            maximo = weditor.lineas
            linea, ok = QInputDialog.getInt(self, self.tr("Ir a línea"),
                                         self.tr("Línea:"), min=1, max=maximo)
            if ok:
                weditor.setCursorPosition(linea - 1, 0)

    def proyecto_nuevo(self):
        dialogo = dialogo_proyecto.DialogoProyecto(self)
        dialogo.show()

    def dragEnterEvent(self, evento):
        data = evento.mimeData()
        if data.hasText():
            # Se acepta el evento de arrastrado
            evento.accept()

    def dropEvent(self, evento):
        self._drop_event(evento)

    def _drop_editor(self, evento):
        self._drop_event(evento)

    def _drop_event(self, evento):
        data = evento.mimeData()
        archivo = data.urls()[0].toLocalFile()
        self.abrir_archivo(archivo)


principal = EditorContainer()