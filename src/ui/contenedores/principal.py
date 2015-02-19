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
    QInputDialog,
    QMessageBox
    )

from PyQt4.QtCore import (
    SIGNAL,
    QFileInfo,
    pyqtSignal
    )

from src.helpers import manejador_de_archivo
from src.helpers.exceptions import EdisIOException
from src.helpers.configuracion import ESettings
from src.ui.editor import (
    editor,
    stack
    )
from src.ui.main import EDIS
from src.ui.widgets import popup_busqueda
from src.ui.contenedores import selector
from src.ui.dialogos import (
    dialogo_propiedades,
    dialogo_log,
    dialogo_proyecto,
    dialogo_reemplazo
    )
from src.ui import start_page
from src.helpers import logger
from src.tools import code_analizer

log = logger.edis_logger.get_logger(__name__)
ERROR = log.error


class EditorContainer(QWidget):

    # Señales
    closedFile = pyqtSignal(int)
    cursorPosition = pyqtSignal(int, int, int)
    fileModified = pyqtSignal(bool)
    updateSymbols = pyqtSignal('QString')
    fileChanged = pyqtSignal('QString')
    openedFile = pyqtSignal('QString')

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
                     self.save_file)
        self.connect(self.stack, SIGNAL("archivo_modificado(bool)"),
                     self._archivo_modificado)
        self.connect(self.stack, SIGNAL("archivo_cerrado(int)"),
                     self._archivo_cerrado)
        self.connect(self.stack, SIGNAL("recentFile(QStringList)"),
                     self.update_recents_files)
        self.connect(self, SIGNAL("fileChanged(QString)"),
                     self.update_symbols)

    def update_symbols(self, s):
        """ Se obtienen los símbolos en un diccionario """

        weditor = self.devolver_editor()
        source_code = weditor.texto
        source_sanitize = code_analizer.sanitize_source_code(source_code)
        symbols = code_analizer.parse_symbols(source_sanitize)
        symbols_widget = EDIS.lateral("symbols")
        symbols_widget.update_symbols(symbols)

    def update_recents_files(self, recents_files):
        menu = EDIS.componente("menu_recent_file")
        self.connect(menu, SIGNAL("triggered(QAction*)"),
                     self._open_recent_file)
        menu.clear()
        for _file in recents_files:
            menu.addAction(_file)

    def _open_recent_file(self, accion):
        self.open_file(accion.text())

    def get_recents_files(self):
        menu = EDIS.componente('menu_recent_file')
        actions = menu.actions()
        recents_files = []
        for filename in actions:
            recents_files.append(filename.text())
        return recents_files

    def _archivo_cerrado(self, index):
        self.closedFile.emit(index)
        self.cambiar_widget(index)

    def _archivo_modificado(self, value):
        self.fileModified.emit(value)

    def __archivo_guardado(self, weditor):
        self.updateSymbols.emit(weditor.nombre)
        self.fileModified.emit(False)

    def cambiar_widget(self, index):
        self.stack.cambiar_widget(index)
        weditor = self.devolver_editor()
        if weditor is not None:
            self.fileChanged.emit(weditor.nombre)

    def add_editor(self, filename=""):
        if not filename:
            filename = "Nuevo_archivo"
        weditor = editor.crear_editor(filename)
        self.agregar_widget(weditor)
        # Señales del Editor
        weditor.modificationChanged[bool].connect(self.stack.editor_modificado)
        weditor.cursorPositionChanged[int, int].connect(self.actualizar_cursor)
        weditor.archivo_guardado.connect(self.__archivo_guardado)
        weditor.dropSignal.connect(self._drop_editor)
        weditor.setFocus()
        return weditor

    def open_file(self, nombre="", posicion_cursor=None):
        filtro = "Archivos C/C++(*.cpp *.c);;ASM(*.s);;HEADERS(*.h);;(*.*)"
        if not nombre:
            carpeta = os.path.expanduser("~")
            editor_widget = self.devolver_editor()
            if editor_widget and editor_widget.nombre:
                carpeta = self.__ultima_carpeta_visitada(editor_widget.nombre)
            archivos = QFileDialog.getOpenFileNames(self, self.trUtf8(
                                                    "Abrir archivo"),
                                                    carpeta, filtro)
        else:
            archivos = [nombre]
        try:
            for archivo in archivos:
                if not self.__archivo_abierto(archivo):
                    self.stack.no_esta_abierto = False
                    contenido = manejador_de_archivo.get_file_content(archivo)
                    nuevo_editor = self.add_editor(archivo)
                    nuevo_editor.texto = contenido
                    nuevo_editor.nombre = archivo
                    if posicion_cursor is not None:
                        linea, columna = posicion_cursor
                        nuevo_editor.setCursorPosition(linea, columna)
                    self.fileChanged.emit(archivo)
                    self.openedFile.emit(archivo)
        except EdisIOException as error:
            ERROR('Error opening file: %s', error)
            QMessageBox.critical(self, self.tr('Error al abrir el archivo'),
                                    str(error))
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

    def add_start_page(self):
        """ Agrega la página de inicio al stack """

        _start_page = start_page.StartPage()
        self.stack.insertWidget(0, _start_page)
        self.stack.setCurrentIndex(0)

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

    def close_file(self):
        self.stack.cerrar()

    def close_all(self):
        self.stack.cerrar_todo()

    def close_all_others(self):
        self.stack.cerrar_demas()

    def selector(self):
        if self.devolver_editor() is not None:
            selector_ = selector.Selector(self)
            selector_.show()

    def save_file(self):
        #FIXME: Controlar con try-except
        weditor = self.devolver_editor()
        if weditor.es_nuevo:
            return self.save_file_as(weditor)
        nombre_archivo = weditor.nombre
        codigo_fuente = weditor.texto
        manejador_de_archivo.escribir_archivo(nombre_archivo, codigo_fuente)
        weditor.nombre = nombre_archivo
        weditor.guardado()

    def save_file_as(self, weditor):
        #FIXME: Controlar con try-except
        carpeta = os.path.expanduser("~")
        nombre_archivo = QFileDialog.getSaveFileName(self,
                self.trUtf8("Guardar archivo"), carpeta)
        if not nombre_archivo:
            return False
        nombre_archivo = manejador_de_archivo.escribir_archivo(nombre_archivo,
                weditor.texto)
        weditor.nombre = nombre_archivo
        self.fileChanged.emit(nombre_archivo)
        weditor.guardado()

    def save_all(self):
        for weditor in self.stack.editores:
            self.save_file(weditor)

    def guardar_seleccionado(self, archivo):
        for i in range(self.stack.contar):
            if self.stack.editor(i).nombre == archivo:
                self.save_file(self.stack.editor(i))

    def archivos_sin_guardar(self):
        return self.stack.archivos_sin_guardar()

    def check_archivos_sin_guardar(self):
        return self.stack.check_archivos_sin_guardar()

    def find(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            dialogo = popup_busqueda.PopupBusqueda(self.devolver_editor())
            dialogo.show()

    def find_and_replace(self):
        dialogo = dialogo_reemplazo.DialogoReemplazo(self)
        dialogo.show()

    def undo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.deshacer()

    def redo(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.rehacer()

    def cut(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.cortar()

    def copy(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.copiar()

    def paste(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.pegar()

    def show_tabs_and_spaces(self):
        tabs_espacios = ESettings.get('editor/mostrarTabs')
        ESettings.set('editor/mostrarTabs', not tabs_espacios)
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.actualizar()

    def show_indentation_guides(self):
        guias = ESettings.get('editor/guias')
        ESettings.set('editor/guias', not guias)
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.actualizar()

    def zoom_in(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_in()

    def zoom_out(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.zoom_out()

    def select_all(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.seleccionar()

    def opened_files(self):
        return self.stack.archivos_abiertos()

    def file_properties(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            dialogo = dialogo_propiedades.FileProperty(weditor, self)
            dialogo.show()

    def archivo_log(self):
        dialogo = dialogo_log.DialogoLog(self)
        dialogo.show()

    def actualizar_cursor(self, line, row):
        weditor = self.devolver_editor()
        lines = weditor.lineas
        self.cursorPosition.emit(line + 1, row + 1, lines)

    def build_source_code(self):
        output = EDIS.componente("output")
        weditor = self.devolver_editor()
        if weditor is not None:
            self.save_file()
            output.build(weditor.nombre)

    def run_binary(self):
        """ Ejecuta el programa objeto """

        output = EDIS.componente("output")
        output.run()

    def build_and_run(self):
        output = EDIS.componente("output")
        weditor = self.devolver_editor()
        if weditor is not None:
            self.save_file()
            output.build_and_run(weditor.nombre)

    def clean_construction(self):
        output = EDIS.componente("output")
        output.clean()

    def stop_program(self):
        output = EDIS.componente("output")
        output.stop()

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

    def indent(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.indentar()

    def unindent(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.quitar_indentacion()

    def to_title(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.a_titulo()

    def duplicate_line(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.duplicar_linea()

    def delete_line(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.eliminar_linea()

    def move_down(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.mover_linea_abajo()

    def move_up(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.mover_linea_arriba()

    def go_to_line(self, linea):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.setCursorPosition(linea, 0)

    def plegar_desplegar(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            weditor.foldAll()

    def show_go_to_line(self):
        weditor = self.devolver_editor()
        if weditor is not None:
            max_lines = weditor.lineas
            line, ok = QInputDialog.getInt(self, self.tr("Ir a línea"),
                                           self.tr("Línea:"), min=1,
                                           max=max_lines)
            if ok:
                weditor.setCursorPosition(line - 1, 0)

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
        self.open_file(archivo)


principal = EditorContainer()