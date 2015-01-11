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
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QSpacerItem
    )

# Módulos QtCore
#from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings

# Módulos EDIS
from src import recursos
from src.helpers.configuracion import ESettings


class ConfiguracionGeneral(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGeneral, self).__init__(parent)
        self.parent = parent
        contenedor = QVBoxLayout(self)

        # Inicio
        grupo_inicio = QGroupBox(self.tr("Al inicio:"))
        box = QVBoxLayout(grupo_inicio)
        self.check_inicio = QCheckBox(self.tr("Mostrar ventana de inicio"))
        self.check_inicio.setChecked(ESettings.get('general/inicio'))
        box.addWidget(self.check_inicio)

        # Al salir
        grupo_salir = QGroupBox(self.tr("Al salir:"))
        box = QVBoxLayout(grupo_salir)
        self.check_al_cerrar = QCheckBox(self.tr("Confirmar al cerrar"))
        box.addWidget(self.check_al_cerrar)
        self.check_dimensiones = QCheckBox(self.tr(
            "Guardar posición y tamaño de la ventana"))
        box.addWidget(self.check_dimensiones)

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
        contenedor.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                            QSizePolicy.Expanding))
        btn_reestablecer.clicked.connect(self._reestablecer)

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        ESettings.set('general/inicio', self.check_inicio.isChecked())
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
