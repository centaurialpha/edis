# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QGraphicsOpacityEffect,
    QFrame
    )
from PyQt4.QtCore import (
    QPropertyAnimation,
    Qt
    )
from PyQt4.Qsci import QsciScintilla


class Minimap(QsciScintilla):

    def __init__(self, weditor):
        QsciScintilla.__init__(self, weditor)
        self._weditor = weditor
        self._indentation = self._weditor._indentation
        self.setLexer(self._weditor.lexer())
        # Configuración Scintilla
        self.setMouseTracking(True)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.SendScintilla(QsciScintilla.SCI_HIDESELECTION, True)
        self.setFolding(QsciScintilla.NoFoldStyle, 1)
        self.setReadOnly(True)
        self.setCaretWidth(0)
        self.setStyleSheet("background: transparent; border: 0px;")
        # Opacity
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.5)
        # Deslizador
        self.slider = Slider(self)
        self.slider.hide()

    def resizeEvent(self, event):
        super(Minimap, self).resizeEvent(event)
        self.slider.setFixedWidth(self.width())
        lines_on_screen = self._weditor.SendScintilla(
            QsciScintilla.SCI_LINESONSCREEN)
        self.slider.setFixedHeight(lines_on_screen * 4)

    def update_geometry(self):
        self.setFixedHeight(self._weditor.height())
        self.setFixedWidth(self._weditor.width() * 0.13)
        x = self._weditor.width() - self.width()
        self.move(x, 0)
        self.zoomIn(-3)

    def update_code(self):
        text = self._weditor.text().replace('\t', ' ' * self._indentation)
        self.setText(text)

    def leaveEvent(self, event):
        super(Minimap, self).leaveEvent(event)
        self.slider.animation.setStartValue(0.2)
        self.slider.animation.setEndValue(0)
        self.slider.animation.start()

    def enterEvent(self, event):
        super(Minimap, self).enterEvent(event)
        if not self.slider.isVisible():
            self.slider.show()
        else:
            self.slider.animation.setStartValue(0)
            self.slider.animation.setEndValue(0.2)
            self.slider.animation.start()


class Slider(QFrame):

    def __init__(self, minimap):
        QFrame.__init__(self, minimap)
        self._minimap = minimap
        self.setStyleSheet("background: gray; border-radius: 3px;")
        # Opacity
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.2)
        # Animación
        self.animation = QPropertyAnimation(self.effect, "opacity")
        self.animation.setDuration(150)
        # Cursor
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        #FIXME: funciona algo loco
        pos = self.mapToParent(event.pos())
        dy = pos.y() - (self.height() / 2)
        if dy < 0:
            dy = 0
        self.move(0, dy)
        pos.setY(pos.y() - event.pos().y())
        self._minimap._weditor.verticalScrollBar().setValue(pos.y())
        self._minimap.verticalScrollBar().setSliderPosition(
                    self._minimap.verticalScrollBar().sliderPosition() + 2)
        self._minimap.verticalScrollBar().setValue(pos.y() - event.pos().y())

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)