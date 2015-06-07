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
    QPixmap,
    QKeySequence,
    QShortcut
    #QSpacerItem,
    #QSizePolicy
    )
from PyQt4.QtCore import Qt
from src.ui.widgets.pyborita import pyborita


class PyboritaWidget(QWidget):

    def __init__(self, parent=None):
        super(PyboritaWidget, self).__init__(parent)
        self.parent = parent
        main_container = QVBoxLayout(self)

        ## Información puntaje
        box_score = QHBoxLayout()
        self._score = "<h2>Puntaje: %s</h2>"
        self.lbl_score = QLabel(self._score % 0)
        self.lbl_score.setStyleSheet("background: #232729")
        self.lbl_score.setAlignment(Qt.AlignCenter)
        box_score.addWidget(self.lbl_score)
        self._max_score = "<h2>Máximo Puntaje: %s</h2>"
        self.lbl_max_score = QLabel(self._max_score % 0)
        self.lbl_max_score.setStyleSheet("background: #232729")
        self.lbl_max_score.setAlignment(Qt.AlignCenter)
        box_score.addWidget(self.lbl_max_score)
        main_container.addLayout(box_score)

        # Snake
        self.frame_snake = pyborita.Pyborita()
        main_container.addWidget(self.frame_snake)
        main_container.setAlignment(Qt.AlignCenter)

        tecla_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        # Conexiones
        tecla_escape.activated.connect(self._mostrar_dialogo)
        self.frame_snake.scoreChanged[int].connect(self.update_score)
        self.frame_snake.highscoreChanged[int].connect(self.update_max_score)

    def _mostrar_dialogo(self):
        self.frame_snake.pause()
        self.dialogo = QDialog()
        self.dialogo.setWindowTitle(self.tr("Pyborita"))
        box = QVBoxLayout(self.dialogo)
        # Acerca de
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
        # Botones
        hbox = QHBoxLayout()
        btn_nuevo_juego = QPushButton(self.tr("Nuevo Juego"))
        hbox.addWidget(btn_nuevo_juego)
        btn_salir = QPushButton(self.tr("Salir"))
        hbox.addWidget(btn_salir)
        box.addLayout(hbox)

        # Conexiones de botones
        btn_nuevo_juego.clicked.connect(self._nuevo_juego)
        btn_salir.clicked.connect(self._close)

        self.dialogo.exec_()
        self.frame_snake.reanude()
        self.frame_snake.setFocus()

    def _nuevo_juego(self):
        self.dialogo.close()
        self.frame_snake.new_game()

    def _close(self):
        self.dialogo.close()
        self.close()
        self.parent.stack.removeWidget(self)

    def update_score(self, value):
        self.lbl_score.setText(self._score % value)

    def update_max_score(self, value):
        self.lbl_max_score.setText(self._max_score % value)
