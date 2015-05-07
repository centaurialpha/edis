# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import bisect

from PyQt4.QtGui import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QToolButton,
    QStackedWidget,
    QMessageBox,
    QIcon,
    QMenu,
    QSizePolicy
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt,
    QSize,
    pyqtSignal
    )

from src.ui.editor import editor
from src.ui.main import Edis


class EditorWidget(QWidget):

    # Señales
    allFilesClosed = pyqtSignal()

    def __init__(self):
        super(EditorWidget, self).__init__()
        self._recents_files = []

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        # Combo container
        self.combo = ComboContainer(self)
        box.addWidget(self.combo)

        # Stacked
        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        self.connect(self.combo.combo_file,
                     SIGNAL("currentIndexChanged(int)"), self.change_item)

    def add_widget(self, widget):
        index = self.stack.addWidget(widget)
        if not self.combo.isVisible():
            self.combo.setVisible(True)
        self.stack.setCurrentIndex(index)

    def add_item_combo(self, text):
        self.combo.combo_file.addItem(text)
        self.combo.combo_file.setCurrentIndex(
            self.combo.combo_file.count() - 1)

    def remove_item_combo(self, index):
        self.combo.combo_file.removeItem(index)

    def change_item(self, index):
        self.stack.setCurrentIndex(index)
        self.emit(SIGNAL("currentWidgetChanged(int)"), index)

    def current_widget(self):
        return self.stack.currentWidget()

    def current_index(self):
        return self.stack.currentIndex()

    def widget(self, index):
        return self.stack.widget(index)

    def count(self):
        return self.stack.count()

    def close_file(self):
        self.remove_widget(self.current_widget(), self.current_index())

    def close_file_project(self, widget, index):
        #FIXME: unir con close file
        self.remove_widget(widget, index)

    def close_all(self):
        for index in range(self.count()):
            self.remove_widget(self.current_widget(), 0)

    def editor_modified(self, value):
        weditor = self.current_widget()
        index = self.current_index()
        self.combo.set_modified(weditor, index, value)

    def _add_to_recent(self, filename):
        if filename == 'Untitled':
            return
        if filename not in self._recents_files:
            self._recents_files.append(filename)
            self.emit(SIGNAL("recentFile(QStringList)"), self._recents_files)

    def check_files_not_saved(self):
        value = False
        for index in range(self.count()):
            weditor = self.widget(index)
            value = value or weditor.is_modified
        return value

    def files_not_saved(self):
        files = []
        for index in range(self.count()):
            weditor = self.widget(index)
            if weditor.is_modified:
                files.append(weditor.filename)
        return files

    def opened_files(self):
        files = []
        for index in range(self.count()):
            weditor = self.widget(index)
            path = weditor.filename
            if path == 'Untitled':
                continue
            files.append(path)
        return files

    def remove_widget(self, widget, index):
        if not isinstance(widget, editor.Editor):
            return
        if index != -1:
            self.stack.setCurrentIndex(index)

            flags = QMessageBox.Yes
            flags |= QMessageBox.No
            flags |= QMessageBox.Cancel

            result = QMessageBox.No
            if widget.is_modified:
                result = QMessageBox.question(self, self.tr(
                    "File not saved"),
                    self.tr("The file <b>{0}</b> "
                            "has unsaved changes. Would you "
                            "like to save them?").format(widget.filename),
                    QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel)
                if result == QMessageBox.Cancel:
                    return
                elif result == QMessageBox.Yes:
                    self.emit(SIGNAL("saveCurrentFile()"))
            self._add_to_recent(widget.filename)
            self.stack.removeWidget(widget)
            self.emit(SIGNAL("fileClosed(int)"), index)
            self.remove_item_combo(index)
            widget.obj_file.stop_system_watcher()
            if self.current_widget() is not None:
                self.current_widget().setFocus()
            else:
                self.allFilesClosed.emit()

    def add_symbols(self, symbols):
        self.combo.add_symbols_combo(symbols)


class ComboContainer(QWidget):

    def __init__(self, parent=None):
        super(ComboContainer, self).__init__()
        self._editor_widget = parent
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        self._lines_symbols = []

        # Basado en la GUI de Qt Creator
        # Combo archivos
        self.combo_file = QComboBox()
        self.combo_file.setIconSize(QSize(14, 14))
        self.combo_file.setContextMenuPolicy(Qt.CustomContextMenu)
        box.addWidget(self.combo_file)
        # Botón cerrar
        btn_close_editor = QToolButton()
        btn_close_editor.setFixedSize(25, 22)
        btn_close_editor.setObjectName("combo-button")
        btn_close_editor.setToolTip(self.tr("Close file"))
        btn_close_editor.setIcon(QIcon(":image/close"))
        btn_close_editor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        box.addWidget(btn_close_editor)
        # Combo símbolos
        self.combo_symbols = QComboBox()
        self.combo_symbols.setIconSize(QSize(14, 14))
        box.addWidget(self.combo_symbols)
        # Label número de línea y columna
        self.label_line_row = QToolButton()
        self.label_line_row.mousePressEvent = self._show_dialog_go_to_line
        self.label_line_row.setObjectName("combo-lines-button")
        self.line_row = "Lin: %s, Col: %s - %s"
        self.label_line_row.setText(self.line_row % (0, 0, 0))
        self.label_line_row.setToolTip(
            self.tr("Click to go to a specific line and column"))
        box.addWidget(self.label_line_row)

        output = Edis.get_component("output")

        # Conexiones
        self.connect(btn_close_editor, SIGNAL("clicked()"),
                     self._close_current_file)
        self.connect(output.salida_, SIGNAL("updateSyntaxCheck(bool)"),
                     self._show_icon_checker)
        self.connect(self.combo_symbols, SIGNAL("activated(int)"),
                     self._go_to_symbol)
        self.connect(self.combo_file,
                     SIGNAL("customContextMenuRequested(const QPoint)"),
                     self._load_menu_combo_file)

    def update_cursor_position(self, line, row, lines):
        self.label_line_row.setText(self.line_row % (line, row, lines))

    def _show_dialog_go_to_line(self, event):
        if event.button() == Qt.LeftButton:
            editor_container = Edis.get_component("principal")
            editor_container.show_go_to_line()

    def _load_menu_combo_file(self, point):
        """ Muestra el menú """

        menu = QMenu()
        editor_container = Edis.get_component("principal")
        save_as_action = menu.addAction(QIcon(":image/save-as"),
                                        self.tr("Save as"))
        reload_action = menu.addAction(QIcon(":image/reload"),
                                       self.tr("Reload"))
        menu.addSeparator()
        compile_action = menu.addAction(QIcon(":image/build"),
                                        self.tr("Build"))
        execute_action = menu.addAction(QIcon(":image/run"),
                                        self.tr("Run"))
        menu.addSeparator()
        close_action = menu.addAction(QIcon(":image/close"),
                                      self.tr("Close file"))

        # Conexiones
        self.connect(save_as_action, SIGNAL("triggered()"),
                     editor_container.save_file_as)
        self.connect(reload_action, SIGNAL("triggered()"),
                     editor_container.reload_file)
        self.connect(compile_action, SIGNAL("triggered()"),
                     editor_container.build_source_code)
        self.connect(execute_action, SIGNAL("triggered()"),
                     editor_container.run_binary)
        self.connect(close_action, SIGNAL("triggered()"),
                     editor_container.close_file)

        menu.exec_(self.mapToGlobal(point))

    def _go_to_symbol(self, index):
        editor_container = Edis.get_component("principal")
        line = self._lines_symbols[index]
        editor_container.go_to_line(line)

    def _show_icon_checker(self, value):
        index = self._editor_widget.current_index()
        icon = QIcon()
        if not value:
            icon = QIcon(":image/bug")
            self.combo_file.setItemIcon(index, icon)
        else:
            self.combo_file.setItemIcon(index, icon)

    def _close_current_file(self):
        current_editor = self._editor_widget.current_widget()
        current_index = self._editor_widget.current_index()
        self._editor_widget.remove_widget(current_editor, current_index)

    def set_modified(self, weditor, index, modified):
        if modified:
            text = " \u2022"  # Bullet caracter
            current_text = self.combo_file.currentText()
            self.combo_file.setItemText(index, current_text + text)
        else:
            text = weditor.filename
            self.combo_file.setItemText(index, text)

    def add_symbols_combo(self, symbols):
        """ Agrega símbolos al combo """

        self.combo_symbols.clear()
        self.combo_symbols.addItem(self.tr("<Select Symbol>"))
        lines = [1]
        for symbol in symbols:

            lines.append(symbol[0])
            to_combo = symbol[1][0]
            if symbol[1][1] == 'function':
                icon = QIcon(":image/function")
            elif symbol[1][1] == 'struct':
                icon = QIcon(":image/struct")
            self.combo_symbols.addItem(icon, to_combo)
        self._lines_symbols = lines

    def move_to_symbol(self, line):
        line += 1
        index = bisect.bisect(self._lines_symbols, line)
        self.combo_symbols.setCurrentIndex(index - 1)
