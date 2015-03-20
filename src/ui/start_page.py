# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import(
    QWidget,
    QVBoxLayout
    )
from PyQt4.QtDeclarative import QDeclarativeView
from PyQt4.QtCore import (
    QUrl,
    QDir
    )

from src import paths


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
        box.addWidget(view)
