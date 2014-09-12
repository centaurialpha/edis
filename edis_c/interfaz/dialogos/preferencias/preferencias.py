#-*- coding: utf-8 -*-

# <Diálogo de configuraciones.>
# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QPushButton,
    QStackedWidget
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from edis_c.interfaz.dialogos.preferencias import (
    preferencias_general,
    preferencias_editor,
    preferencias_gui,
    preferencias_compilacion
    )


class DialogoPreferencias(QDialog):

    def __init__(self, parent=None):
        super(DialogoPreferencias, self).__init__(parent)
        self.setWindowTitle(self.trUtf8("EDIS - Preferencias"))
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        self.combo = QComboBox()
        vLayout.addWidget(self.combo)
        self.stack = Stack()
        vLayout.addWidget(self.stack)
        self.general = preferencias_general.TabGeneral(self)
        self.editor = preferencias_editor.TabEditor()
        self.gui = preferencias_gui.TabGUI(self)
        self.compilacion = preferencias_compilacion.ECTab(self)
        widgets = [
            self.general,
            self.editor,
            self.gui,
            self.compilacion,
            ]

        [self.stack.addWidget(widget) for widget in widgets]
        texto_combo = [
            'General',
            'Editor',
            'GUI',
            'Compilador'
            ]
        [self.combo.addItem(item) for item in texto_combo]

        hLayout = QHBoxLayout()
        self.botonCancelar = QPushButton(self.trUtf8("Cancelar"))
        self.botonGuardar = QPushButton(self.trUtf8("Guardar"))
        layoutBotones = QGridLayout()
        hLayout.addWidget(self.botonCancelar)
        hLayout.addWidget(self.botonGuardar)
        layoutBotones.addLayout(hLayout, 0, 0, Qt.AlignRight)
        vLayout.addLayout(layoutBotones)

        self.connect(self.combo, SIGNAL("currentIndexChanged(int)"),
            lambda: self.cambiar_widget(self.combo.currentIndex()))
        self.connect(self.botonCancelar, SIGNAL("clicked()"), self.close)
        self.connect(self.botonGuardar, SIGNAL("clicked()"), self._guardar)

    def cambiar_widget(self, indice):
        if not self.isVisible():
            self.show()
        self.stack.mostrar_widget(indice)

    def _guardar(self):
        [self.stack.widget(i).guardar() for i in range(self.combo.count())]
        self.close()


class Stack(QStackedWidget):

    def __init__(self):
        super(Stack, self).__init__()

    def setCurrentIndex(self, indice):
        QStackedWidget.setCurrentIndex(self, indice)

    def mostrar_widget(self, indice):
        self.setCurrentIndex(indice)