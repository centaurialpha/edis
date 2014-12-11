# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QShortcut,
    QKeySequence,
    QHBoxLayout,
    QLineEdit
    )

from PyQt4.QtCore import (
    Qt,
    QSize,
    QPropertyAnimation,
    SIGNAL,
    QPoint
    )


class PopupBusqueda(QDialog):

    def __init__(self, editor):
        QDialog.__init__(self, editor)
        self.editor = editor
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.line = QLineEdit(self)
        self.line.setMinimumWidth(200)
        self.layout.addWidget(self.line)

        # Popup!
        self.setWindowFlags(Qt.Popup)

        escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(escape, SIGNAL("activated()"),
                    self.ocultar)

        point = editor.rect().topRight()
        global_point = editor.mapToGlobal(point)
        self.move(global_point - QPoint(self.width() + 100, 0))

    def ocultar(self):
        self.hide()
        self.editor.stack.currentWidget().setFocus()

    def showEvent(self, e):
        super(PopupBusqueda, self).showEvent(e)
        size = self.size()
        start_size = QSize(size.width(), 10)
        self.resize(start_size)

        # Animación !
        anim = QPropertyAnimation(self.line, 'size', self.line)
        anim.setStartValue(start_size)
        anim.setEndValue(size)
        anim.setDuration(500)
        anim.start()
        self.line.setFocus()
