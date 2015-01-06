# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
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
    QCheckBox
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
from PyQt4.QtCore import (
    QSettings
    )
#from PyQt4.QtCore import QSettings
##from PyQt4.QtCore import QString
#from PyQt4.QtCore import QSize

## Módulos EDIS
from src import recursos
from src.helpers import configuraciones
#from edis.interfaz import distribuidor


class ConfiguracionGUI(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGUI, self).__init__(parent)
        contenedor = QVBoxLayout(self)

        # Widgets laterales
        grupo_lateral = QGroupBox(self.tr("Widgets laterales:"))
        box = QVBoxLayout(grupo_lateral)
        box.setContentsMargins(0, 0, 0, 0)
        self.check_simbolos = QCheckBox(self.tr("Árbol de símbolos"))
        self.check_simbolos.setChecked(configuraciones.SIMBOLOS)
        box.addWidget(self.check_simbolos)
        self.check_navegador = QCheckBox(self.tr("Navegador"))
        self.check_navegador.setChecked(configuraciones.NAVEGADOR)
        box.addWidget(self.check_navegador)
        self.check_explorador = QCheckBox(self.tr("Explorador"))
        self.check_explorador.setChecked(configuraciones.EXPLORADOR)
        box.addWidget(self.check_explorador)

        contenedor.addWidget(grupo_lateral)

    def guardar(self):
        """ Guarda las configuraciones de la GUI. """
        config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        configuraciones.SIMBOLOS = self.check_simbolos.isChecked()
        config.setValue('gui/simbolos', configuraciones.SIMBOLOS)
        if configuraciones.SIMBOLOS:
            pass