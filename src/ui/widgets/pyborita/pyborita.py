# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import random
from PyQt4.QtGui import (
    QFrame,
    QPainter,
    QColor,
    QFont
    )
from PyQt4.QtCore import (
    Qt,
    QBasicTimer,
    pyqtSignal
    )


class Pyborita(QFrame):

    # Señales
    scoreChanged = pyqtSignal(int)
    highscoreChanged = pyqtSignal(int)

    # Tamaño de los bloques
    HEIGHT_BLOCKS = 40
    WIDTH_BLOCKS = 60

    # Direcciones
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, parent=None):
        super(Pyborita, self).__init__(parent)
        self.highscore = 0
        self.is_paused = True
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(800, 600)
        self.new_game()

    def new_game(self):
        self.timer = QBasicTimer()
        self.score = 0
        # Velocidad inicial
        self.speed = 100
        self.scoreChanged.emit(self.score)
        self.current_direction = Pyborita.RIGHT
        # Estructura inicial
        self.snake = [[5, 10], [5, 10]]
        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]
        self.food = []
        self.board = []
        self.len_snake = 2  # Inicia con 2
        self.grow_snake = False
        self.is_over = False
        self._drop_food()
        self.timer.start(self.speed, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Márgen información
        painter.setPen(QColor("#111"))
        painter.setBrush(QColor("#474a3e"))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 10)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Pyborita.HEIGHT_BLOCKS * \
                   self._square_height()

        for pos in self.snake:
            self.draw(painter,
                      rect.left() + pos[0] * self._square_width(),
                      boardtop + pos[1] * self._square_height())
        for pos in self.food:
            self.draw(painter,
                      rect.left() + pos[0] * self._square_width(),
                      boardtop + pos[1] * self._square_height(), True)
        if self.is_over:
            self.game_over(painter, event)

    def draw(self, painter, x, y, food=False):
        """ Dibuja la viborita y la comida """

        if not food:
            color = QColor(25, 200, 0, 160)
        else:
            color = QColor(200, 80, 0, 255)
        painter.setPen(QColor(0xD9D9D9))
        painter.setBrush(color)
        painter.drawRect(x + 1, y + 1, self._square_width(),
                         self._square_height())

    def _square_width(self):
        return self.contentsRect().width() / Pyborita.WIDTH_BLOCKS

    def _square_height(self):
        return self.contentsRect().height() / Pyborita.HEIGHT_BLOCKS

    def _drop_food(self):
        x = random.randint(5, 58)
        y = random.randint(5, 38)
        for pos in self.snake:
            if pos == [x, y]:
                self._drop_food()
        self.food.append([x, y])

    def _move_snake(self):
        if self.current_direction == Pyborita.LEFT:
            self.current_x_head -= 1
            if self.current_x_head < 0:
                self.current_x_head = Pyborita.WIDTH_BLOCKS
        if self.current_direction == Pyborita.RIGHT:
            self.current_x_head += 1
            if self.current_x_head == Pyborita.WIDTH_BLOCKS:
                self.current_x_head = 0
        if self.current_direction == Pyborita.UP:
            self.current_y_head -= 1
            if self.current_y_head == Pyborita.HEIGHT_BLOCKS:
                self.current_y_head = 0
        if self.current_direction == Pyborita.DOWN:
            self.current_y_head += 1
            if self.current_y_head < 0:
                self.current_y_head = Pyborita.HEIGHT_BLOCKS

        self.snake.insert(0, [self.current_x_head, self.current_y_head])
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self._move_snake()
            self.is_collision()
            self.is_suicide()
            self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if self.current_direction != Pyborita.RIGHT:
                self.current_direction = Pyborita.LEFT
        elif key == Qt.Key_Right:
            if self.current_direction != Pyborita.LEFT:
                self.current_direction = Pyborita.RIGHT
        elif key == Qt.Key_Up:
            if self.current_direction != Pyborita.DOWN:
                self.current_direction = Pyborita.UP
        elif key == Qt.Key_Down:
            if self.current_direction != Pyborita.UP:
                self.current_direction = Pyborita.DOWN
        # Pausa
        elif key == Qt.Key_P:
            if not self.is_paused:
                self.pause()
            else:
                self.timer.start(self.speed, self)
                self.is_paused = False
        # Nuevo juego
        elif key == Qt.Key_Space:
            if self.is_over:
                self.new_game()

    def is_collision(self):

        # Compruebo si la viborita colisiona contra las paredes
        right_wall = self.height() * 0.10 - 1
        if self.snake[0][0] == 0 or self.snake[0][0] == right_wall:
            self.is_over = True
        elif self.snake[0][1] == 0 or self.snake[0][1] == 38:
            self.is_over = True

        if self.len_snake == 10:
            self.speed = 50
            self.timer.start(self.speed, self)
        for pos in self.food:
            if pos == self.snake[0]:
                # Aumento el tamaño
                self.len_snake += 1
                # Aumento el score
                self.score += 1
                self.scoreChanged.emit(self.score)
                # Elimino la comida
                self.food.remove(pos)
                self._drop_food()
                self.grow_snake = True

    def is_suicide(self):
        """ Comprueba si la viborita choca contra sí misma """

        head = self.snake[0]  # Cabeza
        tail = self.snake[1:len(self.snake)]  # Cola
        # Si la cabeza coincide con alguna parte (elemento de la lista)
        # de la cola el juego termina
        if head in tail:
            self.is_over = True

    def pause(self):
        """ Pausa el timer """

        self.timer.stop()
        self.is_paused = True
        self.update()

    def reanude(self):
        self.timer.start(self.speed, self)
        self.is_paused = False
        self.update()

    def game_over(self, painter, event):
        self.highscore = max(self.highscore, self.score)
        self.highscoreChanged.emit(self.highscore)
        painter.setFont(QFont('Decorative', 16))
        gameo = painter.drawText(event.rect(), Qt.AlignCenter, "GAME OVER")
        painter.setFont(QFont('Decorative', 8))
        painter.drawText(gameo.x() - 40, gameo.y() + 40,
                         "Presiona espacio para volver a jugar")
        self.timer.stop()
