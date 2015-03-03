# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout
    )

from PyQt4.QtCore import (
    QUrl,
    SIGNAL,
    Qt,
    QDir,
    )

from PyQt4.QtDeclarative import QDeclarativeView

from src import paths
from src.ui.main import EDIS


class Selector(QDialog):

    def __init__(self, parent=None):
        super(Selector, self).__init__(parent,
                                       Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent")
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        # Interfáz QML
        view = QDeclarativeView()
        qml = os.path.join(paths.PATH, "ui", "Selector.qml")
        path = QDir.fromNativeSeparators(qml)
        view.setSource(QUrl.fromLocalFile(path))

        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        box.addWidget(view)

        self.root = view.rootObject()
        self._load()

        self.connect(self.root, SIGNAL("openFile(int)"),
                     self._open_file)
        self.connect(self.root, SIGNAL("animationCompleted()"),
                     self._animation_completed)
        self.connect(self.root, SIGNAL("close()"), self.close)

    def _open_file(self, index):
        editor_container = EDIS.componente("principal")
        editor_container.change_widget(index)
        self.root.close_widget()

    def _load(self):
        editor_container = EDIS.componente("principal")
        files_opened = editor_container.opened_files()
        for _file in files_opened:
            _file = os.path.basename(_file[0])
            self.root.load_file(_file)
        self.root.current_index(editor_container.current_index())
        self.root.start_animation()

    def _animation_completed(self):
        self.root.close_widget()
        self.close()