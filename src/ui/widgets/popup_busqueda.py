# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QHBoxLayout,
    QToolButton,
    QLineEdit,
    QIcon
    )

from PyQt4.QtCore import (
    Qt,
    QPoint
    )

from src import recursos


class PopupBusqueda(QDialog):

    def __init__(self, editor):
        QDialog.__init__(self, editor)
        self.editor = editor
        self.total = 0
        # Popup!
        self.setWindowFlags(Qt.Popup)
        box = QHBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        self.line = Line(self)
        self.line.setMinimumWidth(200)
        box.addWidget(self.line)
        # Botones
        btn_anterior = QToolButton()
        btn_anterior.setIcon(QIcon(":image/down"))
        btn_siguiente = QToolButton()
        btn_siguiente.setIcon(QIcon(":image/up"))
        box.addWidget(btn_anterior)
        box.addWidget(btn_siguiente)

        # Posición
        qpoint = self.editor.rect().topRight()
        global_point = self.editor.mapToGlobal(qpoint)
        self.move(global_point - QPoint(self.width() + 180, 0))

        # Conexiones
        btn_anterior.clicked.connect(self.buscar_anterior)
        btn_siguiente.clicked.connect(self.buscar_siguiente)

    def buscar(self, forward=True, wrap=False):
        weditor = self.editor
        palabra = self.palabra_buscada
        codigo = weditor.texto
        self.total = codigo.count(palabra)
        weditor.buscar(palabra, cs=True, wo=False, wrap=wrap, forward=forward)
        self.line.actualizar(self.total)

    def buscar_siguiente(self):
        self.buscar(wrap=True)

    def buscar_anterior(self):
        self.buscar(forward=False)

    @property
    def palabra_buscada(self):
        return self.line.text()


class Line(QLineEdit):

    def __init__(self, popup):
        super(Line, self).__init__(popup)
        self.popup = popup

    def actualizar(self, total):
        if total == 0:
            self.setStyleSheet(
                'background-color: %s; border-radius: 3px' %
                recursos.TEMA['error'])
        else:
            self.setStyleSheet('color: #dedede')

    def keyPressEvent(self, e):
        super(Line, self).keyPressEvent(e)
        # Incluye 0-9 y a-z
        if e.key() in range(0x30, 0x5b) or e.key() == Qt.Key_Backspace:
            self.popup.buscar()
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.popup.buscar_siguiente()

    def showEvent(self, e):
        super(Line, self).showEvent(e)
        self.setFocus()