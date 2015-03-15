# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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

    def __init__(self, files, editor_container, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Files unsaved!"))
        self._event_ignore = False
        self._editor_container = editor_container
        vLayout = QVBoxLayout(self)
        label = QLabel(self.tr("The following files have been modified. "
                       "Save them?"))
        vLayout.addWidget(label)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        for e, _file in enumerate(files):
            if not _file:
                _file = "untitled"
            self.list_widget.addItem(_file)
            self.list_widget.item(e).setSelected(True)
        vLayout.addWidget(self.list_widget)

        box_buttons = QHBoxLayout()
        btn_nothing = QPushButton(self.tr("None"))
        btn_save = QPushButton(self.tr("Save Selected"))
        btn_cancel = QPushButton(self.tr("Cancel"))
        box_buttons.addWidget(btn_nothing)
        box_buttons.addWidget(btn_save)
        box_buttons.addWidget(btn_cancel)

        vLayout.addLayout(box_buttons)

        self.key_scape = QShortcut(QKeySequence(Qt.Key_Escape), self)

        # Conexiones
        self.connect(self.key_scape, SIGNAL("activated()"), self._ignore)
        self.connect(btn_nothing, SIGNAL("clicked()"), self.close)
        self.connect(btn_save, SIGNAL("clicked()"), self._save)
        self.connect(btn_cancel, SIGNAL("clicked()"), self._ignore)

    def _ignore(self):
        self._event_ignore = True
        self.hide()

    def ignorado(self):
        return self._event_ignore

    def _save(self):
        selected_files = self.list_widget.selectedItems()
        for _file in selected_files:
            filename = _file.text()
            self._editor_container.save_selected(filename)
        self.close()