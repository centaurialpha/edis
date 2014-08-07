#-*- coding: utf-8 -*-

# <Editor/Mini para la visualización del código, basado en NINJA-IDE.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

""" Minimapa """

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextOption
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QGraphicsOpacityEffect

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPropertyAnimation

from edis_c import recursos
from edis_c.nucleo import configuraciones


class MiniMapa(QPlainTextEdit):

    def __init__(self, parent):
        super(MiniMapa, self).__init__(parent)

        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setCenterOnScroll(True)
        self.setMouseTracking(True)
        self.viewport().setCursor(Qt.PointingHandCursor)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setStyleSheet("background: transparent;")

        self.parent = parent
        self.lineas = 0
        self.highlighter = None

        self.connect(self.parent, SIGNAL("updateRequest(const QRect&, int)"),
            self.actualizar_area_visible)

        self.efecto = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efecto)
        self.efecto.setOpacity(0.07)
        self.animacion = QPropertyAnimation(self.efecto, "opacity")

        self.slider = Slider(self)
        self.slider.show()

    def calcular_max(self):
        altura_de_linea = self.parent.cursorRect().height()
        if altura_de_linea > 0:
            self.lineas = self.parent.viewport().height() / altura_de_linea
        self.slider.actualizar_posicion()
        self.actualizar_area_visible()

    def set_code(self, codigo):
        self.setPlainText(codigo)
        self.calcular_max()

    def actualizar_area_visible(self):
        if not self.slider.pressed:
            numero_linea = self.parent.firstVisibleBlock().blockNumber()
            bloque = self.document().findBlockByLineNumber(numero_linea)
            cursor = self.textCursor()
            cursor.setPosition(bloque.position())
            rect = self.cursorRect(cursor)
            self.setTextCursor(cursor)
            self.slider.mover_slider(rect.y())

    def enterEvent(self, event):
        self.animacion.setDuration(400)
        self.animacion.setStartValue(configuraciones.OPAC_MIN)
        self.animacion.setEndValue(configuraciones.OPAC_MAX)
        self.animacion.start()

    def leaveEvent(self, event):
        self.animacion.setDuration(400)
        self.animacion.setStartValue(configuraciones.OPAC_MAX)
        self.animacion.setEndValue(configuraciones.OPAC_MIN)
        self.animacion.start()

    def mousePressEvent(self, event):
        super(MiniMapa, self).mousePressEvent(event)
        cursor = self.cursorForPosition(event.pos())
        self.parent.saltar_a_linea(cursor.blockNumber())

    def resizeEvent(self, event):
        super(MiniMapa, self).resizeEvent(event)
        self.slider.actualizar_posicion()

    def scroll_area(self, pos_p, pos_slider):
        pos_p.setY(pos_p.y() - pos_slider.y())
        cursor = self.cursorForPosition(pos_p)
        self.parent.verticalScrollBar().setValue(cursor.blockNumber())

    def wheelEvent(self, event):
        super(MiniMapa, self).wheelEvent(event)
        self.parent.wheelEvent(event)

    def ajustar_(self):
        self.setFixedHeight(self.parent.height())
        self.setFixedWidth(self.parent.width() * configuraciones.MINI_TAM)
        x = self.parent.width() - self.width()
        self.move(x, 0)
        tam_fuente = int(self.width() / configuraciones.MARGEN)
        if tam_fuente < 1:
            tam_fuente = 1
        fuente = self.document().defaultFont()
        fuente.setPointSize(tam_fuente)
        self.setFont(fuente)
        self.calcular_max()


class Slider(QFrame):

    def __init__(self, parent):
        super(Slider, self).__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

        color = recursos.TEMA_EDITOR['num-seleccionado']
        self.setStyleSheet("background: %s;" % color)
        self.efecto = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efecto)
        self.efecto.setOpacity(0.2)
        self.pressed = False
        self.scroll_margen = None

    def actualizar_posicion(self):
        tam_fuente = QFontMetrics(self.parent.font()).height()
        altura = self.parent.lineas * tam_fuente
        self.setFixedHeight(altura)
        self.setFixedWidth(self.parent.width())
        self.scroll_margen = (altura, self.parent.height() - altura)

    def mover_slider(self, y):
        self.move(0, y)

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.pressed = True
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseReleaseEvent(event)
        self.pressed = False
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        if self.pressed:
            pos = self.mapToParent(event.pos())
            y = pos.y() - (self.height() / 2)
            if y < 0:
                y = 0
            if y < self.scroll_margen[0]:
                self.parent.verticalScrollBar().setSliderPosition(
                    self.parent.verticalScrollBar().sliderPosition() - 2)

            elif y > self.scroll_margen[1]:
                self.parent.verticalScrollBar().setSliderPosition(
                    self.parent.verticalScrollBar().sliderPosition() + 2)

            self.move(0, y)
            self.parent.scroll_area(pos, event.pos())