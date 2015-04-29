# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QPalette,
    QPainter,
    QBrush,
    QColor,
    QPen,
    QLinearGradient
    )

from PyQt4.QtCore import Qt


class LoadingWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.counter = 0

    def showEvent(self, event):
        self.timer = self.startTimer(100)

    def timerEvent(self, event):
        self.counter += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(3):
            x = self.width() / 2.3 + (30 * i)
            y = self.height() / 2
            # Gradiente
            gradient = QLinearGradient(x + 10, x, y + 10, y)
            gradient.setColorAt(0, QColor("black"))
            gradient.setColorAt(1, QColor("gray"))
            painter.setBrush(QBrush(gradient))
            if self.counter / 2 % 3 == i:
                painter.drawEllipse(x, y, 25, 25)
            else:
                painter.drawEllipse(x, y, 20, 20)
        painter.end()