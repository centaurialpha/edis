# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QShortcut,
    QKeySequence,
    QHBoxLayout,
    QLineEdit,
    QLabel
    )

from PyQt4.QtCore import (
    Qt,
    QSize,
    QPropertyAnimation,
    SIGNAL,
    QPoint,
    QObject
    )


class PopupBusqueda(QDialog):

    def __init__(self, editor):
        QDialog.__init__(self, editor)
        self.editor = editor
        self.total = 0
        self.indice = 0
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.line = QLine(self)
        self.line.contador.actualizar(self.indice, self.total)
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
        self.editor.setFocus()

    def buscar(self, weditor):
        #FIXME: Completar
        palabra = self.line.text()
        codigo = weditor.texto
        self.total = codigo.count(palabra)
        weditor.buscar(palabra)
        self.line.contador.actualizar(self.indice, self.total)

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

    def keyPressEvent(self, e):
        super(PopupBusqueda, self).keyPressEvent(e)
        if e.key() == Qt.Key_Return:
            self.close()


class QLine(QLineEdit):

    def __init__(self, popup):
        super(QLine, self).__init__(popup)
        self.popup = popup
        self.contador = Contador(self)

    def keyPressEvent(self, e):
        editor = self.popup.editor
        if editor is None:
            super(QLine, self).keyPressEvent(e)
            return
        if editor and e.key() in (Qt.Key_Enter, Qt.Key_Return):
            pass
        super(QLine, self).keyPressEvent(e)
        if int(e.key()) in range(32, 162) or e.key() == Qt.Key_Backspace:
            self.popup.buscar(editor)


class Contador(QObject):

    def __init__(self, qline):
        QObject.__init__(self)
        self.indice_total = "%s/%s"
        self.qline = qline
        box = QHBoxLayout(qline)
        box.setMargin(0)
        qline.setLayout(box)
        box.addStretch()
        self.contador = QLabel(qline)
        box.addWidget(self.contador)
        self.contador.setText(self.indice_total % (0, 0))

    def actualizar(self, indice, total, buscada=False):
        self.contador.setText(self.indice_total % (indice, total))