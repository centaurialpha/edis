# -*- coding: utf-8 -*-
# EDIS: Entorno de Desarrollo Integrado Simple para C/C++
#
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QToolButton,
    QIcon,
    QToolBar,
    QStackedWidget,
    QPushButton
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL,
    )

from src import recursos
from src.ui.dialogos.preferencias import (
    preferencias_general,
    preferencias_editor,
    preferencias_gui,
    preferencias_compilacion
    )


class Preferencias(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Preferencias - EDIS"))

        self.general = preferencias_general.TabGeneral(self)
        self.editor = preferencias_editor.TabEditor()
        self.gui = preferencias_gui.TabGUI(self)
        self.compilacion = preferencias_compilacion.ECTab(self)

        # valor: texto en combo, clave: instancia de widgets
        self.widgets = OrderedDict([
            ('General', self.general),
            ('Editor', self.editor),
            ('GUI', self.gui),
            ('Compilador', self.compilacion)
            ])

        self.load_ui()

        # Conexiones
        self.connect(self.button_general, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(0))
        self.connect(self.button_editor, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(1))
        self.connect(self.button_gui, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(2))
        self.connect(self.button_compi, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(3))
        self.connect(self.btn_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.btn_guardar, SIGNAL("clicked()"), self._guardar)

    def load_ui(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.button_general = QToolButton()

        self.button_general.setIcon(QIcon(recursos.ICONOS['preferencias']))
        self.button_general.setText("General")
        self.button_general.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_editor = QToolButton()
        self.button_editor.setIcon(QIcon(recursos.ICONOS['edit']))
        self.button_editor.setText("Editor")
        self.button_editor.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_gui = QToolButton()
        self.button_gui.setIcon(QIcon(recursos.ICONOS['gui']))
        self.button_gui.setText("Interfaz")
        self.button_gui.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.button_compi = QToolButton()
        self.button_compi.setIcon(QIcon(recursos.ICONOS['build']))
        self.button_compi.setText("Compilador")
        self.button_compi.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar.addWidget(self.button_general)
        toolbar.addWidget(self.button_editor)
        toolbar.addWidget(self.button_gui)
        toolbar.addWidget(self.button_compi)

        box.addWidget(toolbar)

        self.stack = Stack()
        box.addWidget(self.stack)

        [self.stack.addWidget(widget)
            for widget in list(self.widgets.values())]

        box_buttons = QHBoxLayout()
        self.btn_cancel = QPushButton(self.tr("Cancelar"))
        self.btn_guardar = QPushButton(self.tr("Guardar"))
        grid = QGridLayout()
        grid.addLayout(box_buttons, 0, 0, Qt.AlignRight)
        box_buttons.addWidget(self.btn_cancel)
        box_buttons.addWidget(self.btn_guardar)

        box.addLayout(grid)

    def cambiar_widget(self, index):
        if not self.isVisible():
            self.show()
        self.stack.mostrar_widget(index)

    def _guardar(self):
        [self.stack.widget(i).guardar()
            for i in range(4)]
        self.close()


class Stack(QStackedWidget):

    def __init__(self):
        super(Stack, self).__init__()

    def setCurrentIndex(self, indice):
        QStackedWidget.setCurrentIndex(self, indice)

    def mostrar_widget(self, indice):
        self.setCurrentIndex(indice)