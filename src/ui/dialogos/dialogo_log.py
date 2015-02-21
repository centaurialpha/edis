# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QPlainTextEdit
    )

from src import recursos


class DialogoLog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Log - EDIS"))
        self.setMinimumSize(550, 300)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        self.visualizador = QPlainTextEdit()
        self.visualizador.setReadOnly(True)
        box.addWidget(self.visualizador)
        self.leer_archivo(recursos.LOG)

    def leer_archivo(self, archivo):
        with open(archivo) as f:
            contenido = f.read()
        self.visualizador.setPlainText(contenido)