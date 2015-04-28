# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import random

from PyQt4.QtGui import(
    QWidget,
    QVBoxLayout
    )
from PyQt4.QtDeclarative import QDeclarativeView
from PyQt4.QtCore import (
    QUrl,
    QDir,
    QTimer
    )

from src.core import paths

TEXTS = [
    "Open a file with Ctrl+O",
    "Change editor with Ctrl+M",
    "Create a new project with Ctrl+Shift+N",
    "Find a word in the text with Ctrl+F",
    "Go to a line and/or column with Ctrl+J",
    "Replace a word with Ctrl+H",
    "Share code with Ctrl+P"
    ]


class StartPage(QWidget):
    """ Interfáz QML """

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QDeclarativeView()
        view.setMinimumSize(400, 400)
        qml = os.path.join(paths.PATH, "ui", "StartPage.qml")
        path = QDir.fromNativeSeparators(qml)
        view.setSource(QUrl.fromLocalFile(path))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        self._root = view.rootObject()
        box.addWidget(view)

        self._current_text = ""
        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(7000)
        self.timer.timeout.connect(self._show_text)
        self._show_text()
        self.timer.start()

    def _show_text(self):
        result = random.choice(TEXTS)
        # Para evitar que se repita
        if result != self._current_text:
            self._root.show_text(result)
        self._current_text = result