# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import random

from PyQt4.QtGui import(
    QWidget,
    QVBoxLayout
    )
from PyQt4.QtDeclarative import QDeclarativeView
from PyQt4.QtCore import (
    QUrl,
    QDir,
    QTimer
    )

from src.core import paths

TEXTS = [
    "Abre un archivo con Ctrl+O",
    "Cambia de Editor con Ctrl+M",
    "Crea un nuevo Proyecto con Ctrl+Shift+N",
    "Busca texto en el código con Ctrl+F",
    "Salta a una línea y/o columna con Ctrl+J",
    "Reemplaza texto con Ctrl+H",
    "Comparte el código con Ctrl+P",
    "Compila el código con Ctrl+B",
    "Compila y Ejecuta con Ctrl+F10",
    "\tEncontraste un problema?\nRepórtalo desde el menú Ayuda",
    "Selecciona un texto y presiona TAB para indentar",
    "Comenta una o más líneas con Ctrl+G",
    "Explora el código desde el Árbol de Símbolos",
    "Oculta todos los widgets con F11"
    ]

WELCOME = "Bienvenido a Edis!"


class StartPage(QWidget):
    """ Interfáz QML """

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QDeclarativeView()
        view.setMinimumSize(400, 400)
        qml = os.path.join(paths.PATH, "ui", "StartPage.qml")
        path = QDir.fromNativeSeparators(qml)
        view.setSource(QUrl.fromLocalFile(path))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        self._root = view.rootObject()
        box.addWidget(view)

        self._current_text = ""
        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self._show_welcome_text()
        self.timer.timeout.connect(self._show_text)
        self.timer.start()

    def _show_welcome_text(self):
        self._root.show_text(WELCOME)

    def _show_text(self):
        if not self._current_text:
            self.timer.setInterval(7000)
        result = random.choice(TEXTS)
        # Para evitar que se repita
        if result != self._current_text:
            self._root.show_text(result)
        self._current_text = result