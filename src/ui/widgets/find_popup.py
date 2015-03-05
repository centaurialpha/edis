# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QHBoxLayout,
    QToolButton,
    QIcon
    )

from PyQt4.QtCore import (
    QPoint,
    SIGNAL
    )

from src.ui.widgets import (
    line_edit,
    base_dialog
    )


class PopupBusqueda(base_dialog.BaseDialog):

    def __init__(self, weditor):
        super(PopupBusqueda, self).__init__(weditor)
        self.total = 0
        box = QHBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        self.line = line_edit.CustomLineEdit()
        self.line.setObjectName("popup")
        self.line.setMinimumWidth(200)
        box.addWidget(self.line)
        # Botones
        btn_previous = QToolButton()
        btn_previous.setIcon(QIcon(":image/up"))
        btn_next = QToolButton()
        btn_next.setIcon(QIcon(":image/down"))
        box.addWidget(btn_previous)
        box.addWidget(btn_next)
        # Posición
        self.move(self.global_point - QPoint(self.width() + 180, 0))

        # Conexiones
        self.connect(self.line, SIGNAL("textEdited(QString)"), self._find)
        self.connect(self.line, SIGNAL("returnPressed()"), self._find_next)
        self.connect(btn_previous, SIGNAL("clicked()"), self._find_previous)
        self.connect(btn_next, SIGNAL("clicked()"), self._find_next)

    def _find(self):
        if not self.word:
            return
        weditor = self._weditor
        found = weditor.findFirst(self.word, False, False, False, False,
                                  True, 0, 0, True)
        if self.word:
            self.line.update(found)
        weditor.hilo_ocurrencias.buscar(self.word, weditor.text())

    def _find_next(self):
        weditor = self._weditor
        weditor.findFirst(self.word, False, False, False, True,
                                  True, -1, -1, True)

    def _find_previous(self):
        weditor = self._weditor
        weditor.findFirst(self.word, False, False, False, True,
                          False, -1, -1, True)
        weditor.findNext()

    @property
    def word(self):
        """ Devuelve el texto ingresado en el CustomLineEdit """

        return self.line.text()