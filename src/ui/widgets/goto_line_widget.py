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
        self.line.setText(self.tr("<line>:<column>"))
        self.line.setSelection(0, len(self.line.text()))
        self.line.setObjectName("popup")
        self.line.setMinimumWidth(200)
        box.addWidget(self.line)
        self.move(self.global_point - QPoint(self.width() + 130, 0))

        self.connect(self.line, SIGNAL("returnPressed()"), self._go)

    def _go(self):
        data = self.line.text()
        if data.startswith(':'):
            return
        index = 0
        if ':' in data:
            data = data.split(':')
            if not data[1]:
                return
            line, index = int(data[0]), int(data[1])
        else:
            line = data.split(':')[0]
        self._weditor.setCursorPosition(int(line) - 1, index)
        self.close()
