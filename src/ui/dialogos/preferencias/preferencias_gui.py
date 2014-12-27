# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
#from PyQt4.QtGui import QStyleFactory
from PyQt4.QtGui import QWidget
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
#from PyQt4.QtCore import Qt
#from PyQt4.QtCore import QSettings
##from PyQt4.QtCore import QString
#from PyQt4.QtCore import QSize

## Módulos EDIS
#from src import recursos
#from src.helpers import configuraciones
#from edis.interfaz import distribuidor


class TabGUI(QWidget):

    def __init__(self, parent):
        super(TabGUI, self).__init__(parent)

    def guardar(self):
        """ Guarda las configuraciones de la GUI. """
        pass