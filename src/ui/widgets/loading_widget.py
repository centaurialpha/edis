# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QPalette,
    QPainter,
    QBrush,
    QColor
    )

from PyQt4.QtCore import Qt


class LoadingWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        qpainter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 200)))
        font = qpainter.font()
        font.setPointSize(16)
        qpainter.setFont(font)
        qpainter.drawText(event.rect(), Qt.AlignCenter, "Please wait...")
        qpainter.end()