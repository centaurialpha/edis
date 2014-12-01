# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtGui import (
    QWidget,
    QHBoxLayout,
    QToolButton,
    QLabel,
    QTextCursor,
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

from . import creador_widget
from src.ui.editor.editor import Editor


class PopupBusqueda(QWidget):
    """ Popup de búsqueda basado en QWidget. """

    def __init__(self, parent=None, widget=None):
        QWidget.__init__(self, parent)
        self.tab = parent

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line = Line(self)
        self.line.setMinimumWidth(200)
        self.botonAnterior = QToolButton()
        self.botonAnterior.setAutoRaise(True)
        self.botonAnterior.setIcon(
            creador_widget.get_icono_estandard('ArrowBack'))

        self.botonSiguiente = QToolButton()
        self.botonSiguiente.setAutoRaise(True)
        self.botonSiguiente.setIcon(
            creador_widget.get_icono_estandard('ArrowForward'))

        layout.addWidget(self.line)
        layout.addWidget(self.botonAnterior)
        layout.addWidget(self.botonSiguiente)

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
            self.buscar_siguiente)
        self.connect(self.botonAnterior, SIGNAL("clicked()"),
            self.buscar_anterior)
        self.connect(self.botonSiguiente, SIGNAL("clicked()"),
            self.buscar_siguiente)
        self.connect(self.tecla_escape, SIGNAL("activated()"), self.ocultar)

    def ocultar(self):
        self.hide()
        e = self.tab.currentWidget()
        e.setFocus()

        #e.buscar_match(unicode(self.line.text()), 0)

    def buscar_anterior(self):
        pass
        #e = self.tab.currentWidget()
        #e.buscar_match(unicode(self.line.text()), 1, True)
        #if self.total > 0 and self.indice > 1:
            #self.indice -= 1
        #elif self.total > 0:
            #self.indice = self.total
            #e.moveCursor(QTextCursor.End)
            #e.buscar_match(unicode(self.line.text()), 1, True)
        #self.line.contador_.actualizar(self.indice, self.total)

    def buscar_siguiente(self):
        pass
        #e = self.tab.currentWidget()
        #e.buscar_match(unicode(self.line.text()), 0, True)
        #if self.total > 0 and self.indice < self.total:
            #self.indice += 1
        #elif self.total > 0:
            #self.indice = 1
        #self.line.contador_.actualizar(self.indice, self.total)

    #def buscar_palabras(self, weditor):
        #if type(weditor) is not Editor:
            #return False
        #codigo = weditor.texto
        #texto_buscado = unicode(self.line.text())

        #busqueda = len(texto_buscado) > 0
        #self.total = codigo.count(texto_buscado)
        #if busqueda and self.total > 0:
            ##cursor = weditor.textCursor()
            ##cursor.movePosition(QTextCursor.WordLeft)
            ##cursor.movePosition(QTextCursor.Start, QTextCursor.KeepAnchor)
            ##codigo = unicode(cursor.selectedText())
            #self.indice = codigo.count(texto_buscado)
        #else:
            #self.indice = 0
            #self.total = 0
        #self.line.contador_.actualizar(self.indice, self.total, busqueda)
        #if busqueda:
            #pass

    def buscar(self, editor):
        codigo = editor.texto
        palabra_buscada = self.line.text()
        busqueda = len(palabra_buscada) > 0
        self.total = codigo.count(palabra_buscada)
        if busqueda and self.total > 0:
            self.indice = codigo.count(palabra_buscada)
        else:
            self.indice = 0
            self.total = 0
        self.line.contador_.actualizar(self.indice, self.total, busqueda)
        editor.busqueda(palabra_buscada)

    def keyPressEvent(self, evento):
        """ Evento de teclas """

        pass


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
            self.parent.buscar_siguiente()
            return
        super(Line, self).keyPressEvent(evento)
        if int(evento.key()) in range(32, 162) or \
        evento.key() == Qt.Key_Backspace:
            self.parent.buscar(editor)
            #self.parent.buscar_palabras(editor)


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