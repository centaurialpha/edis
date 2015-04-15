# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import json

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QStackedWidget
    )

from PyQt4.QtCore import (
    SIGNAL,
    QFileInfo,
    pyqtSignal
    )

from src.core import (
    paths,
    object_file
    )
from src.core.exceptions import EdisIOError
from src.core import settings
from src.ui.editor import editor
from src.ui.main import Edis
from src.ui.widgets import (
    find_popup,
    replace_widget,
    goto_line_widget,
    file_selector
    )
#from src.ui.dialogs.preferences import preferences
from src.ui.dialogs import (
    file_properties,
    new_project,
    code_pasting_dialog
    )
from src.ui.containers import editor_widget
from src.ui import start_page
from src.core import logger

log = logger.edis_logger.get_logger(__name__)
ERROR = log.error

# FIXME: Mejorar la forma en la que se muestra/oculta el stacked del editor


class EditorContainer(QWidget):

    # Señales
    closedFile = pyqtSignal(int)
    cursorPosition = pyqtSignal(int, int, int)
    updateSymbols = pyqtSignal('PyQt_PyObject')
    fileChanged = pyqtSignal('QString')
    openedFile = pyqtSignal('QString')

    def __init__(self, edis=None):
        QWidget.__init__(self, edis)
        self.setAcceptDrops(True)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

        # Stacked
        self.stack = QStackedWidget()
        self.box.addWidget(self.stack)

        # Replace widget
        #FIXME: mover esto
        self._replace_widget = replace_widget.ReplaceWidget()
        self._replace_widget.hide()
        self.box.addWidget(self._replace_widget)

        # Editor widget
        self.editor_widget = editor_widget.EditorWidget()

        # Conexiones
        self.connect(self.editor_widget, SIGNAL("saveCurrentFile()"),
                     self.save_file)
        self.connect(self.editor_widget, SIGNAL("fileClosed(int)"),
                     self._file_closed)
        self.connect(self.editor_widget, SIGNAL("recentFile(QStringList)"),
                     self.update_recents_files)
        self.connect(self.editor_widget, SIGNAL("allFilesClosed()"),
                     self.add_start_page)
        self.connect(self.editor_widget, SIGNAL("currentWidgetChanged(int)"),
                     self.change_widget)

        Edis.load_component("principal", self)

    def update_recents_files(self, recents_files):
        """ Actualiza el submenú de archivos recientes """

        menu = Edis.get_component("menu_recent_file")
        self.connect(menu, SIGNAL("triggered(QAction*)"),
                     self._open_recent_file)
        menu.clear()
        for _file in recents_files:
            menu.addAction(_file)

    def _open_recent_file(self, accion):
        """ Abre el archivo desde el menú """

        self.open_file(accion.text())

    def get_recents_files(self):
        """ Devuelve una lista con los archivos recientes en el menú """

        menu = Edis.get_component('menu_recent_file')
        actions = menu.actions()
        recents_files = []
        for filename in actions:
            recents_files.append(filename.text())
        return recents_files

    def _file_closed(self, index):
        self.closedFile.emit(index)

    def _file_modified(self, value):
        self.editor_widget.editor_modified(value)

    def _file_saved(self, filename):
        self.editor_widget.editor_modified(False)
        self.emit(SIGNAL("updateSymbols(QString)"), filename)

    def change_widget(self, index):
        weditor = self.get_active_editor()
        self.editor_widget.combo.combo_file.setCurrentIndex(index)
        if weditor is not None and not weditor.obj_file.is_new:
            self.emit(SIGNAL("updateSymbols(QString)"), weditor.filename)
            self.emit(SIGNAL("fileChanged(QString)"), weditor.filename)
            weditor.setFocus()

    def create_editor(self, obj_file=None, filename=""):
        if obj_file is None:
            obj_file = object_file.EdisFile(filename)
        self.stack.addWidget(self.editor_widget)
        if isinstance(self.stack.widget(0), start_page.StartPage):
            self.remove_widget(self.stack.widget(0))
        weditor = editor.Editor(obj_file)
        self.editor_widget.add_widget(weditor)
        self.editor_widget.add_item_combo(obj_file.filename)
        lateral = Edis.get_component("tab_container")
        if not lateral.isVisible():
            lateral.show()

        # Conexiones
        self.connect(obj_file, SIGNAL("fileChanged(PyQt_PyObject)"),
                     self._file_changed)
        self.connect(weditor, SIGNAL("cursorPositionChanged(int, int)"),
                     self.update_cursor)
        self.connect(weditor, SIGNAL("modificationChanged(bool)"),
                     self._file_modified)
        self.connect(weditor, SIGNAL("fileSaved(QString)"),
                     self._file_saved)
        self.connect(weditor, SIGNAL("linesChanged(int)"),
                     self.editor_widget.combo.move_to_symbol)
        self.connect(weditor, SIGNAL("dropEvent(PyQt_PyObject)"),
                     self._drop_editor)
        self.emit(SIGNAL("fileChanged(QString)"), obj_file.filename)

        weditor.setFocus()

        return weditor

    def _file_changed(self, obj_file):
        filename = obj_file.filename
        flags = QMessageBox.Yes
        flags |= QMessageBox.No
        result = QMessageBox.information(self, self.tr("File Watcher"),
                                         self.tr("File <b>{0}</b> is "
                                         "modified outside the Edis."
                                         "<br><br>Do you want to "
                                         "reload it?".format(filename)), flags)
        if result == QMessageBox.No:
            return
        self.reload_file(obj_file)

    def reload_file(self, obj_file=None):
        weditor = self.get_active_editor()
        if obj_file is None:
            obj_file = weditor.obj_file
        content = obj_file.read()
        if weditor.is_modified:
            result = QMessageBox.information(self, self.tr(
                "File not saved"),
                self.tr("Are you sure you want to reload <b>{0}</b>?"
                        "<br><br>"
                        "Any unsaved changes will be lost.").format(
                            obj_file.filename),
                QMessageBox.Cancel | QMessageBox.Yes)
            if result == QMessageBox.Cancel:
                return
        weditor.setText(content)
        weditor.markerDeleteAll()
        weditor.setModified(False)

    def open_file(self, filename="", cursor_position=None):
        filter_files = "C Files(*.cpp *.c);;ASM(*.s);;HEADERS(*.h);;(*.*)"
        if not filename:
            working_directory = os.path.expanduser("~")
            weditor = self.get_active_editor()
            if weditor and weditor.filename:
                working_directory = self._last_folder(weditor.filename)
            filenames = QFileDialog.getOpenFileNames(self,
                                                     self.tr("Open file"),
                                                     working_directory,
                                                     filter_files)
        else:
            filenames = [filename]
        try:
            for _file in filenames:
                if not self._is_open(_file):
                    #self.editor_widget.not_open = False
                    # Creo el objeto Edis File
                    obj_file = object_file.EdisFile(_file)
                    content = obj_file.read()
                    weditor = self.create_editor(obj_file, _file)
                    weditor.setText(content)
                    # Cuando se setea el contenido en el editor
                    # se emite la señal textChanged() por lo tanto se agrega
                    # el marker, entonces se procede a borrarlo
                    weditor.markerDelete(0, 3)
                    # FIXME: Cursor position not found
                    #if cursor_position is not None:
                        #line, row = cursor_position
                        #weditor.setCursorPosition(line, row)
                    weditor.setModified(False)
                    obj_file.run_system_watcher()
                else:
                    # Se cambia el índice del stacked
                    # para mostrar el archivo que ya fué abierto
                    for index in range(self.editor_widget.count()):
                        editor = self.editor_widget.widget(index)
                        if editor.filename == _file:
                            self.change_widget(index)

                self.emit(SIGNAL("fileChanged(QString)"), _file)
                self.emit(SIGNAL("openedFile(QString)"), _file)
                self.emit(SIGNAL("updateSymbols(QString)"), _file)
        except EdisIOError as error:
            ERROR('Error opening file: %s', error)
            QMessageBox.critical(self, self.tr('Could not open file'),
                                 str(error))
        #self.editor_widget.not_open = True

    def _last_folder(self, path):
        """ Devuelve la última carpeta a la que se accedió """

        return QFileInfo(path).absolutePath()

    def _is_open(self, archivo):
        """
        Retorna True si un archivo ya esta abierto,
        False en caso contrario

        """

        for index in range(self.editor_widget.count()):
            widget = self.editor_widget.widget(index)
            if widget.filename == archivo:
                return True
        return False

    def add_widget(self, widget):
        """ Agrega @widget al stacked """

        self.editor_widget.add_widget(widget)

    def add_start_page(self):
        """ Agrega la página de inicio al stack """

        if settings.get_setting('general/show-start-page'):
            _start_page = start_page.StartPage()
            self.stack.insertWidget(0, _start_page)
            self.stack.setCurrentIndex(0)
        else:
            self.editor_widget.combo.setVisible(False)

    def remove_widget(self, widget):
        """ Elimina el @widget del stacked """

        self.stack.removeWidget(widget)

    def current_widget(self):
        """ Widget actual """

        return self.editor_widget.current_widget()

    def current_index(self):
        return self.editor_widget.current_index()

    def get_active_editor(self):
        """ Devuelve el Editor si el widget actual es una instancia de él,
        de lo contrario devuelve None. """

        widget = self.current_widget()
        if isinstance(widget, editor.Editor):
            return widget
        return None

    def close_file(self):
        self.editor_widget.close_file()

    def close_file_from_project(self, filename):
        #FIXME: revisar
        for index in range(self.editor_widget.count()):
            widget = self.editor_widget.widget(index)
            if widget.filename == filename:
                editor, i = widget, index
        self.editor_widget.close_file_project(editor, i)

    def close_all(self):
        self.editor_widget.close_all()

    def show_selector(self):
        if self.get_active_editor() is not None:
            selector = file_selector.FileSelector(self)
            selector.show()

    def save_file(self, weditor=None):
        if weditor is None:
            weditor = self.get_active_editor()
            if weditor is None:
                return
        if weditor.obj_file.is_new:
            return self.save_file_as(weditor)
        source_code = weditor.text()
        weditor.obj_file.write(source_code)
        weditor.saved()
        # System watcher
        weditor.obj_file.run_system_watcher()
        return weditor.filename

    def save_file_as(self, weditor=None):
        if weditor is None:
            weditor = self.get_active_editor()
            if weditor is None:
                return
        working_directory = os.path.expanduser("~")
        filename = QFileDialog.getSaveFileName(self, self.tr("Save file"),
                                               working_directory)
        if not filename:
            return False
        content = weditor.text()
        weditor.obj_file.write(content, filename)
        weditor.saved()
        weditor.obj_file.run_system_watcher()
        self.emit(SIGNAL("fileChanged(QString)"), filename)
        return filename

    def save_selected(self, filename):
        for index in range(self.editor_widget.count()):
            if self.editor_widget.widget(index).filename == filename:
                self.save_file(self.editor_widget.widget(index))

    def files_not_saved(self):
        return self.editor_widget.files_not_saved()

    def check_files_not_saved(self):
        return self.editor_widget.check_files_not_saved()

    def find(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            dialog = find_popup.PopupBusqueda(self.get_active_editor())
            dialog.show()

    def find_and_replace(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            if self._replace_widget.isVisible():
                self._replace_widget.hide()
                weditor.setFocus()
            else:
                self._replace_widget.show()

    def action_undo(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.undo()

    def action_redo(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.redo()

    def action_cut(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.cut()

    def action_copy(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.copy()

    def action_paste(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.paste()

    def show_tabs_and_spaces(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            tabs_spaces = settings.get_setting('editor/show-tabs-spaces')
            settings.set_setting('editor/show-tabs-spaces', not tabs_spaces)
            weditor.update_options()

    def show_indentation_guides(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            guides = settings.get_setting('editor/show-guides')
            settings.set_setting('editor/show-guides', not guides)
            weditor.update_options()

    def delete_editor_markers(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.markerDeleteAll()

    def action_zoom_in(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.zoom_in()

    def action_zoom_out(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.zoom_out()

    def action_normal_size(self):
        """ Carga el tamaño por default de la fuente """

        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.zoomTo(0)

    def action_select_all(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.selectAll()

    def opened_files(self):
        return self.editor_widget.opened_files()

    def opened_files_for_selector(self):
        self.index_file_selector = 0
        files = []
        for index in range(self.editor_widget.count()):
            weditor = self.editor_widget.widget(index)
            path = weditor.filename
            if not path:
                path = weditor.display + ' (%s)' % self.index_file_selector
                self.index_file_selector += 1
            files.append(path)
        return files

    def get_open_projects(self):
        tree_projects = Edis.get_lateral("tree_projects")
        return tree_projects.get_open_projects()

    def file_properties(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            dialog = file_properties.FileProperty(weditor, self)
            dialog.show()

    def update_cursor(self, line, row):
        weditor = self.get_active_editor()
        lines = weditor.lines()
        self.editor_widget.combo.update_cursor_position(
            line + 1, row + 1, lines)
        self.cursorPosition.emit(line + 1, row + 1, lines)

    def build_source_code(self):
        output = Edis.get_component("output")
        project = Edis.get_lateral("tree_projects")
        weditor = self.get_active_editor()
        if weditor is not None:
            filename = self.save_file()
            if project.sources:
                output.build((filename, project.sources))
            else:
                if filename:
                    output.build((weditor.filename, []))

    def run_binary(self):
        """ Ejecuta el programa objeto """

        output = Edis.get_component("output")
        output.run()

    def build_and_run(self):
        output = Edis.get_component("output")
        weditor = self.get_active_editor()
        if weditor is not None:
            self.save_file()
            output.build_and_run(weditor.filename)

    def clean_construction(self):
        output = Edis.get_component("output")
        output.clean()

    def stop_program(self):
        output = Edis.get_component("output")
        output.stop()

    def action_comment(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.comment()

    def action_uncomment(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.uncomment()

    def action_indent(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.indent_more()

    def action_unindent(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.indent_less()

    def action_to_lowercase(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.to_lowercase()

    def action_to_uppercase(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.to_uppercase()

    def action_to_title(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.to_title()

    def action_duplicate_line(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.duplicate_line()

    def action_delete_line(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.delete_line()

    def action_move_down(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.move_down()

    def action_move_up(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.move_up()

    def go_to_line(self, line):
        weditor = self.get_active_editor()
        if weditor is not None:
            weditor.setCursorPosition(line, 0)

    def show_go_to_line(self):
        weditor = self.get_active_editor()
        if weditor is not None:
            dialog = goto_line_widget.GoToLineDialog(weditor)
            dialog.show()

    def add_symbols_combo(self, symbols):
        self.editor_widget.add_symbols(symbols)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if data.hasText():
            # Se acepta el evento de arrastrado
            event.accept()

    def dropEvent(self, event):
        self._drop_event(event)

    def _drop_editor(self, event):
        self._drop_event(event)

    def _drop_event(self, event):
        data = event.mimeData()
        filename = data.urls()[0].toLocalFile()
        self.open_file(filename)

    def show_settings(self):
        preferences_widget = Edis.get_component("preferences")
        current_widget = self.stack.currentWidget()
        if isinstance(current_widget, preferences_widget.__class__):
            return
        self.connect(preferences_widget,
                     SIGNAL("configurationsClose(PyQt_PyObject)"),
                     lambda widget: self.remove_widget(widget))
        index = self.stack.addWidget(preferences_widget)
        self.stack.setCurrentIndex(index)

    def open_project(self, filename='', edis_project=True):
        if edis_project:
            if not filename:
                filename = QFileDialog.getOpenFileName(self,
                                                       self.tr("Load Project"),
                                                       paths.PROJECT_DIR,
                                                       "Edis file(*.epf)")
                if not filename:
                    return
                project_file = json.load(open(filename))
                project_path = project_file.get('path', '')
            else:
                project_path = os.path.dirname(filename)
        else:
            result = QFileDialog.getExistingDirectory(self,
                                                      self.tr("Select folder"))
            if not result:
                return
            project_path = result
        project_structure = {}
        filter_files = ['.c', '.h']
        for parent, dirs, files in os.walk(project_path):
            files = [fi for fi in files
                     if os.path.splitext(fi)[-1] in filter_files]
            project_structure[parent] = (files, dirs)
        self.emit(SIGNAL("projectOpened(PyQt_PyObject)"),
                  (project_structure, project_path, edis_project, filename))

    def open_directory(self):
        self.open_project(edis_project=False)

    def create_new_project(self):
        project_creator = new_project.NewProjectDialog(self)
        self.connect(project_creator, SIGNAL("projectReady(PyQt_PyObject)"),
                     self._update_data)
        project_creator.show()

    def _update_data(self, data):
        self.emit(SIGNAL("projectReady(PyQt_PyObject)"), data)

    def opened_projects(self):
        pass

    def code_pasting(self):
        if self.get_active_editor() is not None:
            code = self.get_active_editor().text()
            code_pasting = code_pasting_dialog.CodePastingDialog(self, code)
            code_pasting.exec_()


editor_container = EditorContainer()
