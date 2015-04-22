# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QShortcut,
    QKeySequence
    )

from PyQt4.QtCore import (
    Qt,
    QPropertyAnimation,
    QRect,
    QEasingCurve,
    SIGNAL
    )


class BaseDialog(QDialog):

    """ Base para popup dialog en la esquina superior derecha """

    def __init__(self, weditor):
        super(BaseDialog, self).__init__(weditor)
        self._weditor = weditor
        self.line = None
        # Popup
        self.setWindowFlags(Qt.Popup)
        # Posición
        self.qpoint = weditor.rect().topRight()
        self.global_point = weditor.mapToGlobal(self.qpoint)
        # Animación
        self._animation = QPropertyAnimation(self, "geometry")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Linear)

        key_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(key_escape, SIGNAL("activated()"), self._close)

    def showEvent(self, event):
        super(BaseDialog, self).showEvent(event)
        x, y = self.geometry().x(), self.geometry().y()
        self._animation.setStartValue(QRect(x, 0, self.width(), self.height()))
        self._animation.setEndValue(QRect(x, y, self.width(), self.height()))
        self._animation.start()
        self.line.setFocus()

    def _close(self):
        x, y = self.geometry().x(), self.geometry().y()
        self._animation.setStartValue(QRect(x, y, self.width(), self.height()))
        self._animation.setEndValue(QRect(x, 0, self.width(), self.height()))
        self._animation.start()
        self.connect(self._animation, SIGNAL("finished()"), self.close)
