# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton
    )


class DialogoReemplazo(QDialog):

    def __init__(self, parent=None):
        super(DialogoReemplazo, self).__init__(parent)
        self.setWindowTitle(self.tr("Reemplazar"))
        box = QVBoxLayout(self)

        grilla = QGridLayout()
        grilla.addWidget(QLabel(self.tr("Buscar por:")), 0, 0)
        self.linea_busqueda = QLineEdit()
        self.linea_busqueda.setMinimumWidth(350)
        grilla.addWidget(self.linea_busqueda, 0, 1)
        grilla.addWidget(QLabel(self.tr("Reemplazar con:")), 1, 0)
        self.linea_reemplazo = QLineEdit()
        grilla.addWidget(self.linea_reemplazo, 1, 1)
        self.check_cs = QCheckBox(self.tr("Respetar Case Sensitive"))
        grilla.addWidget(self.check_cs, 2, 0)
        self.check_wo = QCheckBox(self.tr("Buscar palabra completa"))
        grilla.addWidget(self.check_wo, 2, 1)

        box_botones = QHBoxLayout()
        box_botones.addStretch(1)
        btn_buscar = QPushButton(self.tr("Buscar"))
        box_botones.addWidget(btn_buscar)
        btn_reemplazar = QPushButton(self.tr("Reemplazar"))
        box_botones.addWidget(btn_reemplazar)
        btn_reemplazar_todo = QPushButton(self.tr("Reemplazar todo"))
        box_botones.addWidget(btn_reemplazar_todo)

        box.addLayout(grilla)
        box.addLayout(box_botones)