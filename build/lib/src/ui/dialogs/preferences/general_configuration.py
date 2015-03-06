# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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

from src.helpers.configurations import ESettings


class GeneralConfiguration(QWidget):

    def __init__(self, parent):
        super(GeneralConfiguration, self).__init__(parent)
        self.parent = parent
        container = QVBoxLayout(self)

        # Inicio
        group_on_start = QGroupBox(self.tr("Al inicio:"))
        box = QVBoxLayout(group_on_start)
        self.check_on_start = QCheckBox(self.tr("Mostrar ventana de inicio"))
        self.check_on_start.setChecked(ESettings.get('general/show-start-page'))
        box.addWidget(self.check_on_start)

        # Al salir
        group_on_exit = QGroupBox(self.tr("Al salir:"))
        box = QVBoxLayout(group_on_exit)
        self.check_on_exit = QCheckBox(self.tr("Confirmar al cerrar"))
        self.check_on_exit.setChecked(
            ESettings.get('general/confirm-exit'))
        box.addWidget(self.check_on_exit)
        self.check_geometry = QCheckBox(self.tr(
            "Guardar posición y tamaño de la ventana"))
        self.check_geometry.setChecked(
            ESettings.get('ventana/store-size'))
        box.addWidget(self.check_geometry)

        # Notificaciones
        group_notifications = QGroupBox(self.tr("Notificaciones:"))
        box = QVBoxLayout(group_notifications)
        self.check_updates = QCheckBox(self.tr("Comprobar actualizaciones"))
        self.check_updates.setChecked(ESettings.get('general/check-updates'))
        box.addWidget(self.check_updates)

        # Reestablecer
        group_restart = QGroupBox(self.tr("Reestablecer:"))
        box = QHBoxLayout(group_restart)
        btn_reestablecer = QPushButton(self.tr("Reestablecer todo"))
        btn_reestablecer.setObjectName("custom")
        box.addWidget(btn_reestablecer)
        box.addStretch(1)

        container.addWidget(group_on_start)
        container.addWidget(group_on_exit)
        container.addWidget(group_notifications)
        container.addWidget(group_restart)
        container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                           QSizePolicy.Expanding))
        btn_reestablecer.clicked.connect(self._restart_configurations)

    def _restart_configurations(self):
        flags = QMessageBox.Cancel
        flags |= QMessageBox.Yes

        result = QMessageBox.question(self, self.tr("Advertencia"),
                                         self.tr("Está seguro de borrar todas "
                                         "las conguraciones?"), flags)
        if result == QMessageBox.Cancel:
            return
        elif result == QMessageBox.Yes:
            ESettings.clear()
            self.parent.close()

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        ESettings.set('general/show-start-page',
                      self.check_on_start.isChecked())
        ESettings.set('ventana/store-size',
                      self.check_geometry.isChecked())
        ESettings.set('general/confirm-exit',
                      self.check_on_exit.isChecked())
        ESettings.set('general/check-updates', self.check_updates.isChecked())