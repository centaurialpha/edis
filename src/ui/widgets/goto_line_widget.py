# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QLineEdit,
    QVBoxLayout
    )

from PyQt4.QtCore import (
    QPoint,
    SIGNAL
    )

from src.ui.widgets import base_dialog


class GoToLineDialog(base_dialog.BaseDialog):

    def __init__(self, editor):
        super(GoToLineDialog, self).__init__(editor)
        box = QVBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        self.line = QLineEdit()
        self.line.setObjectName("popup")
        self.line.setMinimumWidth(200)
        box.addWidget(self.line)
        self.move(self.global_point - QPoint(self.width() + 130, 0))

        self.connect(self.line, SIGNAL("textEdited(QString)"), self._go)
        self.connect(self.line, SIGNAL("returnPressed()"), self.close)

    def _go(self, strline):
        print("LALA")
        if not strline.isdigit():
            return
        line = int(strline) - 1
        self._weditor.setCursorPosition(line, 0)