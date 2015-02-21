# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QAbstractItemView,
    QLabel,
    QShortcut,
    QKeySequence
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )


class DialogSaveFiles(QDialog):

    def __init__(self, files, editor_container):
        super(DialogSaveFiles, self).__init__(editor_container)
        self.setWindowTitle(self.tr("Archivos sin guardar!"))
        self._editor_container = editor_container
        self._event_ignore = False

        vLayout = QVBoxLayout(self)
        label = QLabel(self.tr("Algunos archivos no se han guardado, "
                       "selecciona los que \ndeseas guardar:"))
        vLayout.addWidget(label)
        hLayout = QHBoxLayout()

        self.list_widget = QListWidget()
        [self.list_widget.addItem(item) for item in files]
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        hLayout.addWidget(self.list_widget)

        box_buttons = QVBoxLayout()
        btn_all = QPushButton(self.tr("Todo"))
        btn_nothing = QPushButton(self.tr("Ninguno"))
        btn_save = QPushButton(self.tr("Guardar"))
        btn_cancel = QPushButton(self.tr("Cancelar"))
        btn_not_save = QPushButton(self.tr("No guardar"))
        box_buttons.addWidget(btn_all)
        box_buttons.addWidget(btn_nothing)
        box_buttons.addWidget(btn_save)
        box_buttons.addWidget(btn_not_save)
        box_buttons.addWidget(btn_cancel)

        hLayout.addLayout(box_buttons)
        vLayout.addLayout(hLayout)

        self.key_scape = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self.key_scape, SIGNAL("activated()"), self._ignore)
        self.connect(btn_all, SIGNAL("clicked()"), self._select_all)
        self.connect(btn_nothing, SIGNAL("clicked()"), self._deselect)
        self.connect(btn_save, SIGNAL("clicked()"), self._save)
        self.connect(btn_not_save, SIGNAL("clicked()"), self.close)
        self.connect(btn_cancel, SIGNAL("clicked()"), self._ignore)

    def _ignore(self):
        self._event_ignore = True
        self.hide()

    def ignorado(self):
        return self._event_ignore

    def _select_all(self):
        for item in range(self.list_widget.count()):
            self.list_widget.item(item).setSelected(True)

    def _deselect(self):
        for item in range(self.list_widget.count()):
            self.list_widget.item(item).setSelected(False)

    def _save(self):
        selected_files = self.list_widget.selectedItems()
        for _file in selected_files:
            filename = _file.text()
            self._editor_container.save_selected(filename)
        self.close()