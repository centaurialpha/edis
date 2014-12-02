# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtGui import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QShortcut,
    QKeySequence
    )

from PyQt4.QtCore import (
    Qt,
    QPoint,
    SIGNAL,
    QObject
    )


class PopupBusqueda(QWidget):
    """ Popup de búsqueda rápida basado en QWidget. """

    def __init__(self, parent=None, widget=None):
        QWidget.__init__(self, parent)
        self.tab = parent

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line = Line(self)
        self.line.setMinimumWidth(200)

        layout.addWidget(self.line)

        self.setLayout(layout)
        self.adjustSize()

        # Popup !
        self.setWindowFlags(Qt.Popup)

        # Posición respecto al widget (ToolButton)
        point = widget.rect().bottomRight()
        global_point = widget.mapToGlobal(point)
        self.move(global_point - QPoint(self.width() + 30, 0))

        self.total = 0
        self.indice = 0
        self.line.contador_.actualizar(self.indice, self.total)

        self.tecla_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(self.line, SIGNAL("returnPressed()"),
            self.buscar)
        self.connect(self.tecla_escape, SIGNAL("activated()"), self.ocultar)

    def ocultar(self):
        self.hide()
        e = self.tab.currentWidget()
        e.setFocus()

    @property
    def palabra_buscada(self):
        """ Devuelve el texto del QLineEdit """

        return self.line.text()

    def buscar(self, editor):
        if editor:
            indice, total = editor.busqueda(self.palabra_buscada)
            self.line.contador_.actualizar(indice, total,
                                            len(self.palabra_buscada) > 0)


class Line(QLineEdit):
    """ LineEdit basado en QLineEdit """

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.parent = parent
        self.contador_ = Contador(self)

    def keyPressEvent(self, evento):
        editor = self.parent.tab.currentWidget()
        if editor is None:
            super(Line, self).keyPressEvent(evento)
            return
        if editor and evento.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.parent.buscar(editor)
            return
        super(Line, self).keyPressEvent(evento)
        if int(evento.key()) in range(32, 162) or \
        evento.key() == Qt.Key_Backspace:
            self.parent.buscar(editor)


class Contador(QObject):
    """ Contandor para el line edit """

    def __init__(self, line):
        QObject.__init__(self)
        self.line_edit = line
        box = QHBoxLayout(line)
        box.setMargin(0)
        line.setLayout(box)
        box.addStretch()
        self.contador = QLabel(line)
        box.addWidget(self.contador)

    def actualizar(self, indice, total, buscada=False):
        mensaje = self.tr("%1/%2").arg(indice).arg(total)
        self.contador.setText(mensaje)
        ESTILO = {
            'True': True if indice == 0 and total == 0 and buscada else False
            }

        if ESTILO['True']:
            self.line_edit.setStyleSheet(
                "background-color: #e73e3e;color: white;border-radius: 3px;")
        else:
            self.line_edit.setStyleSheet("color: gray;")