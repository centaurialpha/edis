# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QIcon,
    QToolBar,
    QStackedWidget,
    QPushButton
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL,
    QSize
    )

from src.ui.edis_main import EDIS
from src import recursos
from src.ui.dialogos.preferencias import (
    preferencias_general,
    preferencias_editor,
    #preferencias_gui,
    #preferencias_compilacion
    )


class Preferencias(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowTitle(self.tr("Preferencias - EDIS"))
        self.setMinimumSize(700, 500)
        self.general = preferencias_general.ConfiguracionGeneral(self)
        self.editor = preferencias_editor.TabEditor()
        #self.gui = preferencias_gui.TabGUI(self)
        #self.compilacion = preferencias_compilacion.ECTab(self)

        # valor: texto en combo, clave: instancia de widgets
        self.widgets = OrderedDict([
            ('General', self.general),
            ('Editor', self.editor)])
            #('GUI', self.gui),
            #('Compilador', self.compilacion)
            #])

        self.load_ui()

        # Conexiones
        self.connect(self.button_general, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(0))
        self.connect(self.button_editor, SIGNAL("clicked()"),
                    lambda: self.cambiar_widget(1))
        #self.connect(self.button_gui, SIGNAL("clicked()"),
                    #lambda: self.cambiar_widget(2))
        #self.connect(self.button_compi, SIGNAL("clicked()"),
                    #lambda: self.cambiar_widget(3))
        self.connect(self.btn_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.btn_guardar, SIGNAL("clicked()"), self._guardar)

        EDIS.cargar_componente("preferencias", self)

    def load_ui(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(40, 40))
        toolbar.setObjectName("preferencias")
        #toolbar.setStyleSheet("background: #47484b")
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.button_general = ToolButton("General",
                                        recursos.ICONOS['general'])
        self.button_editor = ToolButton("Editor",
                                        recursos.ICONOS['edit'])
        #self.button_gui = ToolButton("Interfáz", recursos.ICONOS['gui'])
        #self.button_compi = ToolButton("Compilador", recursos.ICONOS['build'])

        toolbar.addWidget(self.button_general)
        toolbar.addWidget(self.button_editor)
        #toolbar.addWidget(self.button_gui)
        #toolbar.addWidget(self.button_compi)

        box.addWidget(toolbar)

        self.stack = Stack()
        box.addWidget(self.stack)

        [self.stack.addWidget(widget)
            for widget in list(self.widgets.values())]

        box_buttons = QHBoxLayout()
        box_buttons.setMargin(5)
        box_buttons.setSpacing(10)
        box_buttons.addStretch(1)
        self.btn_cancel = QPushButton(self.tr("Cancelar"))
        self.btn_guardar = QPushButton(self.tr("Guardar"))
        box_buttons.addWidget(self.btn_cancel)
        box_buttons.addWidget(self.btn_guardar)

        box.addLayout(box_buttons)

    def cambiar_widget(self, index):
        if not self.isVisible():
            self.show()
        self.stack.mostrar_widget(index)

    def _guardar(self):
        [self.stack.widget(i).guardar()
            for i in range(self.stack.count())]
        self.close()


class Stack(QStackedWidget):

    def __init__(self):
        super(Stack, self).__init__()

    def setCurrentIndex(self, indice):
        QStackedWidget.setCurrentIndex(self, indice)

    def mostrar_widget(self, indice):
        self.setCurrentIndex(indice)


class ToolButton(QToolButton):

    def __init__(self, texto, icono):
        super(ToolButton, self).__init__()
        self.setStyleSheet("color: #bfbfbf")
        self.setText(self.trUtf8(texto))
        self.setIcon(QIcon(icono))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


preferencias = Preferencias()