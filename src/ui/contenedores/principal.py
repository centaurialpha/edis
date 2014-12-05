# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QHBoxLayout,
    QPlainTextEdit
    )


class EditorContainer(QWidget):

    def __init__(self, edis):
        QWidget.__init__(self, edis)
        box = QHBoxLayout(self)
        box.addWidget(QPlainTextEdit())