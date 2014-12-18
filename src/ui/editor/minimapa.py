# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

#TODO: Cambiar QPlainTextEdit por QsciScintilla
#FIXME: Resaltado de sintaxis

from PyQt4.QtGui import (
    QPlainTextEdit,
    QFrame,
    QFontMetrics,
    QGraphicsOpacityEffect
    )

from PyQt4.QtCore import (
    QPropertyAnimation,
    Qt
    )


class MiniMapa(QPlainTextEdit):

    lineas = 0

    def __init__(self, editor):
        super(MiniMapa, self).__init__(editor)
        # Configuración QPlainTextEdit
        self.setReadOnly(True)
        self.setMouseTracking(True)

        self.editor = editor
        self.setStyleSheet("background: transparent; color: white")
        # Deslizador
        self.deslizador = Deslizador(self)
        self.deslizador.show()

        # Efecto y animación
        self.efecto = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efecto)
        self.efecto.setOpacity(0.07)
        self.animacion = QPropertyAnimation(self.efecto, "opacity")

    def codigo(self, codigo):
        self.setPlainText(codigo)
        self.altura_lineas()
        self.area()

    def area(self):
        if not self.deslizador.presionado:
            linea, c = self.editor.devolver_posicion_del_cursor()
            bloque = self.document().findBlockByNumber(linea)
            cursor = self.textCursor()
            cursor.setPosition(bloque.position())
            rec = self.cursorRect(cursor)
            self.setTextCursor(cursor)
            self.deslizador.mover(rec.y())

    def redimensionar(self):
        ancho = self.editor.width() * 0.17
        altura = self.editor.height()
        self.setFixedSize(ancho, altura)
        self.mover(self.editor.width() - self.width(), 0)
        #FIXME: Márgen de línea
        tam_fuente = self.width() / 80
        fuente = self.document().defaultFont()
        fuente.setPointSize(tam_fuente)
        self.setFont(fuente)
        self.altura_lineas()

    def altura_lineas(self):
        altura = self.editor.altura_lineas
        if altura > 0:
            self.lineas = self.editor.viewport().height() / altura
        self.deslizador.ajustar()

    def mover(self, x, y):
        self.move(x, y)

    def scroll_area(self, pos, pos_des):
        pos.setY(pos.y() - pos_des.y())
        cursor = self.cursorForPosition(pos)
        self.editor.verticalScrollBar().setValue(cursor.blockNumber())

    def resizeEvent(self, e):
        super(MiniMapa, self).resizeEvent(e)
        self.deslizador.ajustar()

    def enterEvent(self, e):
        self.animacion.setDuration(400)
        self.animacion.setStartValue(0.07)
        self.animacion.setEndValue(0.30)
        self.animacion.start()

    def leaveEvent(self, e):
        self.animacion.setDuration(400)
        self.animacion.setStartValue(0.30)
        self.animacion.setEndValue(0.07)
        self.animacion.start()


class Deslizador(QFrame):

    def __init__(self, minimapa):
        super(Deslizador, self).__init__(minimapa)
        self.minimapa = minimapa
        self.efecto = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efecto)
        self.efecto.setOpacity(0.4)
        self.setStyleSheet("background: blue")
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.presionado = False
        self.scroll_margen = None

    def ajustar(self):
        fuente = QFontMetrics(self.minimapa.font()).height()
        altura = self.minimapa.lineas * fuente
        self.setFixedHeight(altura)
        self.setFixedWidth(self.minimapa.width())
        self.scroll_margen = (altura, self.minimapa.height() - altura)

    def mover(self, y):
        self.move(0, y)

    def mousePressEvent(self, e):
        super(Deslizador, self).mousePressEvent(e)
        self.presionado = True
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, e):
        super(Deslizador, self).mouseReleaseEvent(e)
        self.presionado = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, e):
        super(Deslizador, self).mouseMoveEvent(e)
        if self.presionado:
            posicion = self.mapToParent(e.pos())
            y = posicion.y() - self.height() / 2
            if y < 0:
                y = 0
            if y < self.scroll_margen[0]:
                self.minimapa.verticalScrollBar().setSliderPosition(
                    self.minimapa.verticalScrollBar().sliderPosition() - 2)
            elif y < self.scroll_margen[1]:
                self.minimapa.verticalScrollBar().setSliderPosition(
                    self.minimapa.verticalScrollBar().sliderPosition() + 2)
            self.move(0, y)
            self.minimapa.scroll_area(posicion, e.pos())