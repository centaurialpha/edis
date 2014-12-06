# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QStackedLayout
    )

from src.ui.editor import editor


class EditorContainer(QWidget):

    def __init__(self, edis):
        QWidget.__init__(self, edis)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        #self.combo = combo_widget.ComboWidget(self)
        #vbox.addWidget(self.combo)

        self.stack = QStackedLayout()
        vbox.addLayout(self.stack)

    def agregar_editor(self, nombre=""):
        if not nombre:
            nombre = "Nuevo_archivo"
        editor_widget = editor.crear_editor(nombre_archivo=nombre)
        #self.combo.agregar_item(nombre)
        self.stack.addWidget(editor_widget)