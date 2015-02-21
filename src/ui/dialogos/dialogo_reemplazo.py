# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
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

from PyQt4.QtCore import SIGNAL

from src.ui.main import EDIS

#FIXME: Que no se comporte como dialogo
#FIXME: Buscar antes de la posición del cursor


class ReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super(ReplaceDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Reemplazar"))
        box = QVBoxLayout(self)

        grilla = QGridLayout()
        grilla.addWidget(QLabel(self.tr("Buscar por:")), 0, 0)
        self._search_line = QLineEdit()
        self._search_line.setMinimumWidth(350)
        grilla.addWidget(self._search_line, 0, 1)
        grilla.addWidget(QLabel(self.tr("Reemplazar con:")), 1, 0)
        self._replace_line = QLineEdit()
        grilla.addWidget(self._replace_line, 1, 1)
        self.check_cs = QCheckBox(self.tr("Respetar Case Sensitive"))
        self.check_cs.setChecked(True)
        grilla.addWidget(self.check_cs, 2, 0)
        self.check_wo = QCheckBox(self.tr("Buscar palabra completa"))
        self.check_wo.setChecked(True)
        grilla.addWidget(self.check_wo, 2, 1)

        box_buttons = QHBoxLayout()
        box_buttons.addStretch(1)
        btn_find = QPushButton(self.tr("Buscar"))
        box_buttons.addWidget(btn_find)
        btn_replace = QPushButton(self.tr("Reemplazar"))
        box_buttons.addWidget(btn_replace)
        btn_replace_all = QPushButton(self.tr("Reemplazar todo"))
        box_buttons.addWidget(btn_replace_all)

        box.addLayout(grilla)
        box.addLayout(box_buttons)

        self.connect(btn_replace, SIGNAL("clicked()"), self._replace)
        self.connect(btn_find, SIGNAL("clicked()"), self._find)
        self.connect(btn_replace_all, SIGNAL("clicked()"), self._replace_all)

    def _replace(self):
        editor_container = EDIS.componente("principal")
        weditor = editor_container.get_active_editor()
        weditor.replace_word(self.palabra_buscada, self.palabra_reemplazo)
        weditor.buscar(self.palabra_buscada, cs=self.cs, wo=self.wo, wrap=False, forward=True)

    def _replace_all(self):
        editor_container = EDIS.componente("principal")
        weditor = editor_container.get_active_editor()
        weditor.buscar(self.palabra_buscada, cs=self.cs, wo=self.wo)
        weditor.replace_word(self.palabra_buscada, self.palabra_reemplazo, True)

    def _find(self):
        editor_container = EDIS.componente("principal")
        weditor = editor_container.get_active_editor()
        weditor.buscar(self.palabra_buscada)

    @property
    def cs(self):
        return self.check_cs.isChecked()

    @property
    def wo(self):
        return self.check_wo.isChecked()

    @property
    def palabra_buscada(self):
        return self._search_line.text()

    @property
    def palabra_reemplazo(self):
        return self._replace_line.text()