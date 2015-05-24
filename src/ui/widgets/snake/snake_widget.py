# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Éste módulo es TOP SECRET!

"""

from PyQt4.QtGui import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QPixmap
    #QSpacerItem,
    #QSizePolicy
    )
from PyQt4.QtCore import Qt
from src.ui.widgets.snake import snake


class SnakeWidget(QWidget):

    def __init__(self, parent=None):
        super(SnakeWidget, self).__init__(parent)
        self.parent = parent
        main_container = QVBoxLayout(self)

        ## Información puntaje
        box_score = QHBoxLayout()
        self._score = "<h2>Puntaje: %s</h2>"
        self.lbl_score = QLabel(self._score % 0)
        self.lbl_score.setAlignment(Qt.AlignCenter)
        box_score.addWidget(self.lbl_score)
        self._max_score = "<h2>Máximo Puntaje: %s</h2>"
        self.lbl_max_score = QLabel(self._max_score % 0)
        self.lbl_max_score.setAlignment(Qt.AlignCenter)
        box_score.addWidget(self.lbl_max_score)
        main_container.addLayout(box_score)

        # Snake
        self.frame_snake = snake.Snake()
        main_container.addWidget(self.frame_snake)
        main_container.setAlignment(Qt.AlignCenter)

        # Botones
        box_botones = QHBoxLayout()
        btn_new_game = QPushButton(self.tr("Nuevo Juego"))
        box_botones.addWidget(btn_new_game)
        btn_exit = QPushButton(self.tr("Salir"))
        box_botones.addWidget(btn_exit)
        btn_about = QPushButton(self.tr("Pyborita"))
        box_botones.addWidget(btn_about)
        main_container.addLayout(box_botones)

        # Conexiones
        self.frame_snake.scoreChanged[int].connect(self.update_score)
        self.frame_snake.highscoreChanged[int].connect(self.update_max_score)
        btn_new_game.clicked.connect(self.frame_snake.new_game)
        btn_exit.clicked.connect(self._close)
        btn_about.clicked.connect(self._about_pyborita)

    def _close(self):
        self.close()
        self.parent.stack.removeWidget(self)

    def update_score(self, value):
        self.lbl_score.setText(self._score % value)

    def update_max_score(self, value):
        self.lbl_max_score.setText(self._max_score % value)

    def _about_pyborita(self):
        self.frame_snake.pause()
        dialog = About()
        dialog.exec_()
        self.frame_snake.reanude()
        self.frame_snake.setFocus()


class About(QDialog):

    def __init__(self):
        super(About, self).__init__()
        self.setWindowTitle(self.tr("Acerca de Pyborita"))
        box = QVBoxLayout(self)

        logo_pyborita = QLabel()
        logo_pyborita.setPixmap(QPixmap(":image/pyborita"))
        logo_pyborita.setAlignment(Qt.AlignCenter)
        box.addWidget(logo_pyborita)

        description = QLabel(self.tr("<b>Pyborita</b> es un clon de Snake "
                            "desarrollado por<br>Gabriel Acosta en Python"
                            " usando PyQt para la GUI.<br><br>Copyright (C) "
                            "<2015> Gabriel Acosta - Gabo<br>"
                            "License: GPLv3"))
        box.addWidget(description)