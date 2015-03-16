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
    QListWidget,
    QApplication,
    QPushButton,
    QStackedWidget,
    QColor,
    QLabel,
    QInputDialog,
    )
from PyQt4.QtCore import SIGNAL

from PyQt4.Qsci import QsciScintilla

from src.helpers import file_manager
from src import (
    paths,
    recursos
    )

doc_stylesheet = "http://qt-project.org/doc/qt-4.8/stylesheet-examples.html"


class ThemeConfiguration(QWidget):

    def __init__(self):
        super(ThemeConfiguration, self).__init__()
        # Stacked
        self.stacked = QStackedWidget()
        box = QVBoxLayout(self)
        box.addWidget(self.stacked)
        # Theme selection widget
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(QLabel(self.tr("Choose a Style Sheet:")))
        self.list_of_themes = QListWidget()
        self._update_list_of_themes()
        vbox.addWidget(self.list_of_themes)
        self.stacked.addWidget(container)
        # Theme creator widget
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        link_doc = QLabel(self.tr("Documentation and examples: <a href='{0}'>"
                                  "<span style='color: lightblue;'>{1}</span>"
                                  "</a>").format(
                                  doc_stylesheet, doc_stylesheet))
        vbox.addWidget(link_doc)
        self.theme_creator = ThemeEditor()
        vbox.addWidget(self.theme_creator)
        self.stacked.addWidget(container)
        # Box botones
        box_btn = QHBoxLayout()
        box_btn.addStretch(1)
        self.btn_preview = QPushButton(self.tr("Preview"))
        #self.btn_preview.setVisible(False)
        box_btn.addWidget(self.btn_preview)
        self.btn_save_theme = QPushButton(self.tr("Save style"))
        self.btn_save_theme.setVisible(False)
        box_btn.addWidget(self.btn_save_theme)
        self.btn_create_new_theme = QPushButton(self.tr("Create a style!"))
        box_btn.addWidget(self.btn_create_new_theme)
        box.addLayout(box_btn)

        # Conexiones
        self.connect(link_doc, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
        self.connect(self.btn_create_new_theme, SIGNAL("clicked()"),
                     self._change_widget)
        self.connect(self.btn_preview, SIGNAL("clicked()"),
                     self._preview_theme)
        self.connect(self.btn_save_theme, SIGNAL("clicked()"),
                     self._save_theme)

    def _change_widget(self):
        if self.stacked.currentIndex() == 0:
            self.stacked.setCurrentIndex(1)
            self.theme_creator.setFocus()
            self.btn_create_new_theme.setText(self.tr("Styles"))
            self.btn_preview.setVisible(True)
            self.btn_save_theme.setVisible(True)

        else:
            self.stacked.setCurrentIndex(0)
            self.btn_create_new_theme.setText(self.tr("Create a style!"))
            self.btn_preview.setVisible(False)
            self.btn_save_theme.setVisible(False)

    def _update_list_of_themes(self):
        """ Actualiza el QListWidget con los temas disponibles """

        path = os.path.join(paths.PATH, "extras", "temas")
        themes = [theme.split('.')[0].title() for theme in os.listdir(path)]
        for theme in os.listdir(paths.EDIS):
            if os.path.splitext(theme)[-1] == '.qss':
                themes.append(theme.split('.')[0].title())
        self.list_of_themes.addItems(themes)

    def _preview_theme(self):
        """ Previsualización del estilo """

        if not self.theme_creator.isVisible():
            # Stack 1
            text = self.list_of_themes.currentItem().text()
            theme = '%s.qss' % text.lower()
            if text == 'Default' or text == 'Edark':
                path_theme = os.path.join(paths.PATH, "extras", "temas", theme)
            else:
                path_theme = os.path.join(paths.EDIS, theme)
            with open(path_theme, 'r') as t:
                style = t.read()
        else:
            # Stack 2
            style = self.theme_creator.text()
        QApplication.instance().setStyleSheet(style)

    def _save_theme(self):
        """ Guarda el tema creado por el editor """

        name, ok = QInputDialog.getText(self, "", self.tr("Name:"))
        if ok:
            content = self.theme_creator.text()
            name = "%s.qss" % name
            filename = os.path.join(paths.EDIS, name)
            file_manager.write_file(filename, content)
            self._update_list_of_themes()

    def guardar(self):
        pass


class ThemeEditor(QsciScintilla):

    def __init__(self):
        super(ThemeEditor, self).__init__()
        # Configuración Scintilla
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, 40)
        self.setPaper(QColor(recursos.TEMA['FondoEditor']))
        self.setColor(QColor(recursos.TEMA['Color']))
        self.setMarginsBackgroundColor(QColor(recursos.TEMA['FoldMarginBack']))
        self.setMarginsForegroundColor(QColor(recursos.TEMA['FoldMarginFore']))
        self.setCaretForegroundColor(QColor('darkGray'))