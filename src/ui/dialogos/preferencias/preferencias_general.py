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
    QHBoxLayout,
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
        self.check_al_cerrar.setChecked(
            ESettings.get('general/confirmarSalida'))
        box.addWidget(self.check_al_cerrar)
        self.check_dimensiones = QCheckBox(self.tr(
            "Guardar posición y tamaño de la ventana"))
        self.check_dimensiones.setChecked(
            ESettings.get('ventana/guardarDimensiones'))
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

    def _reestablecer(self):
        bands = QMessageBox.Cancel
        bands |= QMessageBox.Yes

        resultado = QMessageBox.question(self, self.tr("Advertencia"),
                                        self.tr("Está seguro de borrar todas "
                                        "las conguraciones?"), bands)
        if resultado == QMessageBox.Cancel:
            return
        elif resultado == QMessageBox.Yes:
            ESettings.borrar()
            self.parent.close()

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        ESettings.set('general/inicio', self.check_inicio.isChecked())
        ESettings.set('ventana/guardarDimensiones',
                      self.check_dimensiones.isChecked())
        ESettings.set('general/confirmarSalida',
                      self.check_al_cerrar.isChecked())