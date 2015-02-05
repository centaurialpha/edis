# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import(
    QWidget,
    QVBoxLayout
    )
from PyQt4.QtDeclarative import QDeclarativeView
from PyQt4.QtCore import QUrl


class StartPage(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QDeclarativeView()
        view.setMinimumSize(400, 400)
        view.setSource(QUrl("src/ui/StartPage/StartPage.qml"))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        box.addWidget(view)