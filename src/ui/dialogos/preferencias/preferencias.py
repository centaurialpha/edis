# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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

from src.ui.main import EDIS
from src.ui.dialogos.preferencias import (
    preferencias_general,
    preferencias_editor,
    #preferencias_gui,
    #preferencias_ejecucion
    )

#FIXME: Ejecución, compilación


class Preferencias(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setMinimumWidth(715)
        self.setWindowTitle(self.tr("Preferencias - EDIS"))
        self.general = preferencias_general.ConfiguracionGeneral(self)
        self.editor = preferencias_editor.EditorConfiguration()
        #self.gui = preferencias_gui.ConfiguracionGUI(self)
        #self._ejecucion = preferencias_ejecucion.ConfiguracionEjecucion(self)

        # valor: texto en combo, clave: instancia de widgets
        self.widgets = OrderedDict([
            ('General', self.general),
            ('Editor', self.editor)])
            #('GUI', self.gui),
            #('Ejecucion', self._ejecucion)])
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
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.button_general = ToolButton("General", ":image/general")
        self.button_editor = ToolButton("Editor", ":image/edit")
        #self.button_gui = ToolButton("Interfáz", ":image/gui")
        #self.button_compi = ToolButton("Ejecución", ":image/build")

        toolbar.addWidget(self.button_general)
        toolbar.addWidget(self.button_editor)
        #toolbar.addWidget(self.button_gui)
        #toolbar.addWidget(self.button_compi)

        box.addWidget(toolbar)

        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        [self.stack.addWidget(widget)
            for widget in list(self.widgets.values())]

        box_buttons = QHBoxLayout()
        box_buttons.setMargin(10)
        box_buttons.setSpacing(10)
        box_buttons.addStretch(1)
        self.btn_cancel = QPushButton(self.tr("Cancelar"))
        self.btn_guardar = QPushButton(self.tr("Guardar"))
        box_buttons.addWidget(self.btn_cancel)
        box_buttons.addWidget(self.btn_guardar)

        box.addLayout(box_buttons)

    def mostrar(self):
        self.stack.setCurrentIndex(0)
        self.show()

    def cambiar_widget(self, index):
        if not self.isVisible():
            self.show()
        self.stack.setCurrentIndex(index)

    def _guardar(self):
        [self.stack.widget(i).guardar()
            for i in range(self.stack.count())]
        self.close()


class ToolButton(QToolButton):

    def __init__(self, texto, icono):
        super(ToolButton, self).__init__()
        self.setStyleSheet("color: #bfbfbf")
        self.setText(self.trUtf8(texto))
        self.setIcon(QIcon(icono))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)