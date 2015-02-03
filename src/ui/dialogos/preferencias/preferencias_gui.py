# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    #QHBoxLayout,
    QGroupBox,
    QCheckBox,
    QSpacerItem,
    QSizePolicy
    )
#from PyQt4.QtGui import QStyleFactory
#from PyQt4.QtGui import QVBoxLayout
#from PyQt4.QtGui import QSizePolicy
#from PyQt4.QtGui import QPushButton
#from PyQt4.QtGui import QLabel
#from PyQt4.QtGui import QComboBox
#from PyQt4.QtGui import QGroupBox
#from PyQt4.QtGui import QHBoxLayout
#from PyQt4.QtGui import QIcon
#from PyQt4.QtGui import QToolBar
#from PyQt4.QtGui import QActionGroup
#from PyQt4.QtGui import QApplication
#from PyQt4.QtGui import QListWidget

## Módulos QtCore
#from PyQt4.QtCore import (
    #QSettings
    #)
#from PyQt4.QtCore import QSettings
##from PyQt4.QtCore import QString
#from PyQt4.QtCore import QSize

## Módulos EDIS
#from src import recursos
#from src.helpers import configuraciones
from src.helpers.configuracion import ESettings


class ConfiguracionGUI(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGUI, self).__init__(parent)
        contenedor = QVBoxLayout(self)

        # Widgets laterales
        grupo_lateral = QGroupBox(self.tr("Widgets laterales:"))
        box = QVBoxLayout(grupo_lateral)
        self.check_simbolos = QCheckBox(self.tr("Árbol de símbolos"))
        self.check_simbolos.setChecked(ESettings.get('gui/simbolos'))
        box.addWidget(self.check_simbolos)
        self.check_navegador = QCheckBox(self.tr("Navegador"))
        self.check_navegador.setChecked(ESettings.get('gui/navegador'))
        box.addWidget(self.check_navegador)
        self.check_explorador = QCheckBox(self.tr("Explorador"))
        self.check_explorador.setChecked(ESettings.get('gui/explorador'))
        box.addWidget(self.check_explorador)
        contenedor.addWidget(grupo_lateral)

        contenedor.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                            QSizePolicy.Expanding))

    def guardar(self):
        """ Guarda las configuraciones de la GUI. """

        ESettings.set('gui/simbolos', self.check_simbolos.isChecked())
        ESettings.set('gui/navegador', self.check_navegador.isChecked())
        ESettings.set('gui/explorador', self.check_explorador.isChecked())