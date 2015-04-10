# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import webbrowser

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QPushButton,
    QColor,
    QLabel,
    QInputDialog,
    QComboBox,
    QGroupBox,
    QSpacerItem,
    QSizePolicy
    )
from PyQt4.QtCore import SIGNAL

from PyQt4.Qsci import QsciScintilla

from src import (
    paths,
    editor_scheme
    )
from src.core import settings

doc_stylesheet = "http://qt-project.org/doc/qt-4.8/stylesheet-examples.html"
scheme = editor_scheme.get_scheme(settings.get_setting('editor/scheme'))


class ThemeConfiguration(QWidget):

    def __init__(self):
        super(ThemeConfiguration, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        # Style Sheet
        group1 = QGroupBox(self.tr("Edis Schemes:"))
        vbox = QVBoxLayout(group1)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Choose a Style Sheet:")))
        self.combo_styles = QComboBox()
        self._update_combo()
        index = self.combo_styles.findText(
            settings.get_setting('window/style-sheet'))
        self.combo_styles.setCurrentIndex(index)
        hbox.addWidget(self.combo_styles, 1)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Editor scheme:")))
        self.combo_editor_scheme = QComboBox()
        self.combo_editor_scheme.addItems(['Edis', 'Komodo'])
        scheme = settings.get_setting('editor/scheme')
        index = 0
        if scheme != 'edis':
            index = 1
        self.combo_editor_scheme.setCurrentIndex(index)
        hbox.addWidget(self.combo_editor_scheme, 1)
        vbox.addLayout(hbox)
        vbox.addWidget(QLabel(self.tr("Need restart to see changes")))
        # Create editor
        group2 = QGroupBox(self.tr("Create a Style Sheet:"))
        vbox = QVBoxLayout(group2)
        hbox = QHBoxLayout()
        link_doc = QLabel(self.tr("Documentation and examples: <a href='{0}'>"
                                  "<span style='color: #0197FD;'>{1}</span>"
                                  "</a>").format(
                                      doc_stylesheet, doc_stylesheet))
        hbox.addWidget(link_doc)
        self.btn_save_theme = QPushButton(self.tr("Save"))
        self.btn_save_theme.setEnabled(False)
        hbox.addWidget(self.btn_save_theme)
        self.btn_preview = QPushButton(self.tr("Preview"))
        self.btn_preview.setEnabled(False)
        hbox.addWidget(self.btn_preview)
        self.theme_creator = ThemeEditor()
        self.theme_creator.setMinimumHeight(self.height())
        vbox.addLayout(hbox)
        vbox.addWidget(self.theme_creator)

        # Add groups
        box.addWidget(group1)
        box.addWidget(group2)
        box.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                    QSizePolicy.Expanding))

        # Conexiones
        self.connect(link_doc, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
        self.connect(self.theme_creator, SIGNAL("modificationChanged(bool)"),
                     self._state_of_buttons)
        self.connect(self.btn_preview, SIGNAL("clicked()"), self._preview)
        self.connect(self.btn_save_theme, SIGNAL("clicked()"),
                     self._save_style_sheet)
        self.connect(self.combo_styles, SIGNAL("currentIndexChanged(int)"),
                     self._change_style_sheet)

    def _update_combo(self):
        self.combo_styles.addItems(['Default', 'Edark'])
        list_dir = os.listdir(paths.EDIS)
        list_styles = [i.split('.')[0]for i
                       in list_dir
                       if os.path.splitext(i)[-1] == '.qss']
        self.combo_styles.insertItems(2, list_styles)

    def _state_of_buttons(self, value):
        self.btn_save_theme.setEnabled(value)
        self.btn_preview.setEnabled(value)

    def _change_style_sheet(self, index):
        style_sheet = None
        path = None
        if index == 1:
            path = os.path.join(paths.PATH, "extras",
                                "theme", "edark.qss")
        elif index != 0:
            style = self.combo_styles.currentText() + '.qss'
            path = os.path.join(paths.EDIS, style)
        if path is not None:
            with open(path, mode='r') as f:
                style_sheet = f.read()
        QApplication.instance().setStyleSheet(style_sheet)

    def _preview(self):
        style = self.theme_creator.text()
        QApplication.instance().setStyleSheet(style)

    def _save_style_sheet(self):
        filename, ok = QInputDialog.getText(self, "", self.tr("Name:"))
        if ok:
            new_style_sheet = self.theme_creator.text()
            path = os.path.join(paths.EDIS, filename + '.qss')
            with open(path, mode='w') as f:
                f.write(new_style_sheet)

    def guardar(self):
        style_sheet = self.combo_styles.currentText()
        settings.set_setting('window/style-sheet', style_sheet)
        editor_scheme = self.combo_editor_scheme.currentText()
        if editor_scheme != 'edis':
            editor_scheme = editor_scheme.lower()
        settings.set_setting('editor/scheme', editor_scheme)


class ThemeEditor(QsciScintilla):

    def __init__(self):
        super(ThemeEditor, self).__init__()
        # Configuración Scintilla
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, 40)
        self.setPaper(QColor(scheme['BackgroundEditor']))
        self.setColor(QColor(scheme['Color']))
        self.setMarginsBackgroundColor(QColor(scheme['SidebarBack']))
        self.setMarginsForegroundColor(QColor(scheme['SidebarFore']))
        self.setCaretForegroundColor(QColor('darkGray'))
