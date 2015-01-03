# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
#from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QGroupBox
#from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QCheckBox
#from PyQt4.QtGui import QSpinBox
#from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
#from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QMessageBox
#from PyQt4.QtGui import QSpacerItem
#from PyQt4.QtGui import QSizePolicy

# Módulos QtCore
#from PyQt4.QtCore import Qt
from PyQt4.QtCore import (
    QSettings
    )

# Módulos EDIS
from src import recursos
from src.helpers import (
    configuraciones,
    #manejador_de_archivo
    )


class ConfiguracionGeneral(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGeneral, self).__init__(parent)
        self.parent = parent
        contenedor = QVBoxLayout(self)

        # Inicio
        grupo_inicio = QGroupBox(self.tr("Al inicio:"))
        box = QHBoxLayout(grupo_inicio)
        self.check_inicio = QCheckBox(self.tr("Mostrar ventana de inicio"))
        self.check_inicio.setChecked(configuraciones.INICIO)
        box.addWidget(self.check_inicio)

        # Al salir
        grupo_salir = QGroupBox(self.tr("Al salir:"))
        box = QHBoxLayout(grupo_salir)
        self.check_al_cerrar = QCheckBox(self.tr("Confirmar al cerrar"))
        box.addWidget(self.check_al_cerrar)

        # Reestablecer
        grupo_reestablecer = QGroupBox(self.tr("Reestablecer:"))
        box = QHBoxLayout(grupo_reestablecer)
        btn_reestablecer = QPushButton(self.tr("Reestablecer todo"))
        btn_reestablecer.setObjectName("custom")
        box.addWidget(btn_reestablecer)
        box.addStretch(1)

        contenedor.addWidget(grupo_inicio)
        contenedor.addWidget(grupo_salir)
        contenedor.addWidget(grupo_reestablecer)

        btn_reestablecer.clicked.connect(self._reestablecer)

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        configuraciones.INICIO = self.check_inicio.isChecked()
        config.setValue('general/inicio', self.check_inicio.isChecked())

    def _reestablecer(self):
        bands = QMessageBox.Cancel
        bands |= QMessageBox.Yes

        resultado = QMessageBox.question(self, self.tr("Advertencia"),
                                        self.tr("Está seguro de borrar todas "
                                        "las conguraciones?"), bands)
        if resultado == QMessageBox.Cancel:
            return
        elif resultado == QMessageBox.Yes:
            config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
            config.clear()
            self.parent.close()
