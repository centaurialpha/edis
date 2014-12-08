# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStyle,
    QLabel,
    QComboBox,
    QWidget,
    QStackedLayout,
    QSizePolicy,
    )

from PyQt4.QtCore import (
    SIGNAL,
    pyqtSignal
    )

from src.ui.edis_main import EDIS
from src.ui.editor import editor


class Frame(QFrame):

    cambio_editor = pyqtSignal(int)

    def __init__(self):
        QFrame.__init__(self)
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.combo = QComboBox()
        box.addWidget(self.combo)

        self.posicion_cursor = "Lin: %d / Col: %d"
        self.lbl_cursor = QLabel(self.posicion_cursor % (0, 0))
        self.lbl_cursor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        box.addWidget(self.lbl_cursor)

        self.btn_cerrar = QPushButton(self.style().standardIcon(
                                        QStyle.SP_DialogCloseButton), '')
        self.btn_cerrar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        box.addWidget(self.btn_cerrar)

        self.combo.currentIndexChanged[int].connect(self.current_changed)

    def actualizar_linea_columna(self, linea, columna):
        self.lbl_cursor.setText(self.posicion_cursor % (linea, columna))

    def agregar_item(self, texto):
        self.combo.addItem(texto)
        self.combo.setCurrentIndex(self.combo.count() - 1)

    def current_changed(self, indice):
        self.cambio_editor.emit(indice)


class EditorWidget(QWidget):

    def __init__(self, parent=None):
        super(EditorWidget, self).__init__()
        self.parent = parent
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.no_esta_abierto = True
        self.editores = []

        self.frame = Frame()
        self.frame.setEnabled(False)
        vbox.addWidget(self.frame)

        self.stack = QStackedLayout()
        vbox.addLayout(self.stack)

        self.principal = EDIS.componente("principal")

        self.connect(self.frame, SIGNAL("cambio_editor(int)"),
                    self.cambiar_widget)

    def agregar_editor(self, nombre):
        self.frame.setEnabled(True)
        editor_ = editor.crear_editor(nombre)
        self.editores.append(editor_)
        self.frame.agregar_item(nombre)
        self.connect(editor_, SIGNAL("cursorPositionChanged(int, int)"),
                    self._actualizar_cursor)
        self.connect(editor_, SIGNAL("modificationChanged(bool)"),
                    self._editor_modificado)
        self.stack.addWidget(editor_)
        self.stack.setCurrentWidget(editor_)
        return editor_

    def _actualizar_cursor(self, linea, columna):
        self.frame.actualizar_linea_columna(linea + 1, columna)

    def _editor_modificado(self, valor=True):
        combo = self.frame.combo
        wid = self.stack.currentWidget()
        if isinstance(wid, editor.Editor) and valor and self.no_esta_abierto:
            combo.setItemText(combo.currentIndex(), '*' + combo.currentText())
        else:
            texto = combo.currentText().split('*')[-1]
            combo.setItemText(combo.currentIndex(), texto)

    def cambiar_widget(self, indice):
        self.stack.setCurrentIndex(indice)

    def resizeEvent(self, e):
        super(EditorWidget, self).resizeEvent(e)
        self.setFixedHeight(self.parent.height())

    def currentWidget(self):
        return self.stack.currentWidget()