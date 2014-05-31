#-*- coding: utf-8 -*-

"""
Configuraciones

"""
from PyQt4.QtCore import QSettings

from side_c import recursos

MARGEN = 80
MOSTRAR_MARGEN = True

qsettings = QSettings(recursos.CONFIGURACIONES_PATH, QSettings.IniFormat)

MARGEN = qsettings.value('configuraciones/editor/margenLinea', 80, type=int)
MOSTRAR_MARGEN = qsettings.value(
    'configuraciones/editor/mostrarMargen', True, type=bool)