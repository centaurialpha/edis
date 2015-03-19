# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QGraphicsOpacityEffect
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL,
    QPropertyAnimation
    )

from src.ui.main import Edis

#FIXME:


class FileSelector(QDialog):

    def __init__(self, parent=None):
        super(FileSelector, self).__init__(parent,
                                           Qt.Dialog | Qt.FramelessWindowHint)
        self.setObjectName("file-selector")
        self._files = {}
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, "opacity")
        self.animation.setDuration(1500)
        box = QVBoxLayout(self)
        box.setSpacing(30)
        self.list_of_files = QListWidget()
        self.list_of_files.setObjectName("list-selector")
        box.addWidget(self.list_of_files)
        self.label_path = QLabel()
        box.addWidget(self.label_path)
        self._load_files()

        self.connect(self.list_of_files,
                    SIGNAL("itemSelectionChanged()"),
                    self._update_label)
        self.connect(self.list_of_files,
                     SIGNAL("itemActivated(QListWidgetItem*)"),
                     self._open_file)
        self.connect(self.list_of_files,
                     SIGNAL("itemEntered(QListWidgetItem*)"),
                     self._open_file)

    def _load_files(self):
        """ Carga los archivos abiertos en la lista """

        editor_container = Edis.get_component("principal")
        opened_files = editor_container.opened_files_for_selector()
        for _file in opened_files:
            base_name = os.path.basename(_file)
            self._files[base_name] = _file
            self.list_of_files.addItem(base_name)
        index = editor_container.current_index()
        self.list_of_files.setCurrentRow(index)
        self._update_label()

    def _update_label(self):
        """ Actualiza el QLabel """

        item = self.list_of_files.currentItem()
        show_in_label = self._files.get(item.text())
        self.label_path.setText(show_in_label)

    def _open_file(self, item):
        """ Cambia de archivo en el stacked """

        editor_container = Edis.get_component("principal")
        index = self.list_of_files.row(item)
        editor_container.editor_widget.change_item(index)
        self.close()

    def showEvent(self, event):
        super(FileSelector, self).showEvent(event)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()