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

""" Preferencias """

# Módulos Python
#import os
#import copy

# Módulos QtGui
#from PyQt4.QtGui import QWidget
#from PyQt4.QtGui import QListWidget
#from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTabWidget
#from PyQt4.QtGui import QListView
#from PyQt4.QtGui import QListWidgetItem
#from PyQt4.QtGui import QIcon
#from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
#from PyQt4.QtCore import QSettings

# Módulos EDIS
#from edis_c import recursos
#from edis_c.nucleo import configuraciones
#from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.dialogos.preferencias import preferencias_general
from edis_c.interfaz.dialogos.preferencias import preferencias_editor
from edis_c.interfaz.dialogos.preferencias import preferencias_gui
from edis_c.interfaz.dialogos.preferencias import preferencias_compilacion
#from edis_c.interfaz.dialogos.preferencias import preferencias_tema
#from edis_c.interfaz.dialogos.preferencias import creador_te    ma


class DialogoConfiguracion(QDialog):
    """ Clase QDialog preferencias """

    def __init__(self, parent=None):
        super(DialogoConfiguracion, self).__init__(parent)
        self.setWindowTitle(self.trUtf8("EDIS-C Preferencias"))
        self.setMaximumSize(QSize(0, 0))

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        self.tabs = Tab()
        self.general = preferencias_general.TabGeneral(self)
        self.editor = preferencias_editor.TabEditor()
        self.gui = preferencias_gui.TabGUI(self)
        self.compilacion = preferencias_compilacion.ECTab(self)

        self.tabs.addTab(self.general, self.trUtf8("General"))
        self.tabs.addTab(self.editor, self.trUtf8("Editor"))
        self.tabs.addTab(self.gui, self.trUtf8("GUI"))
        self.tabs.addTab(self.compilacion, self.trUtf8("Compilador"))

        layoutH = QHBoxLayout()
        self.boton_guardar = QPushButton(self.trUtf8("Guardar"))
        self.boton_cancelar = QPushButton(self.trUtf8("Cancelar"))

        layoutH.addWidget(self.boton_cancelar)
        layoutH.addWidget(self.boton_guardar)

        grilla = QGridLayout()
        grilla.addLayout(layoutH, 0, 0, Qt.AlignRight)

        layoutV.addWidget(self.tabs)
        layoutV.addLayout(grilla)

        self.boton_cancelar.clicked.connect(self.cancelar)
        self.boton_guardar.clicked.connect(self.guardar_)

    def cancelar(self):
        self.close()

    def guardar_(self):
        [self.tabs.widget(i).guardar() for i in range(self.tabs.count())]
        self.close()


class Tab(QTabWidget):
    """ Clase Tab """

    def __init__(self):
        super(Tab, self).__init__()
        self.setMovable(False)
        self.setTabPosition(QTabWidget.East)