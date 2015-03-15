# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QToolButton,
    QIcon,
    QCheckBox
    )

from PyQt4.QtCore import SIGNAL

from src.ui.widgets import line_edit
from src.ui.main import Edis


class ReplaceWidget(QDialog):

    def __init__(self):
        super(ReplaceWidget, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        box.setSpacing(2)

        self._cs = False

        find_layout = QHBoxLayout()
        self._line_search = line_edit.CustomLineEdit()
        find_layout.addWidget(self._line_search)
        btn_back = QToolButton()
        btn_back.setIcon(QIcon(":image/back"))
        find_layout.addWidget(btn_back)
        btn_forward = QToolButton()
        btn_forward.setIcon(QIcon(":image/forward"))
        find_layout.addWidget(btn_forward)
        self._check_cs = QCheckBox(self.tr("Case sensitive"))
        find_layout.addWidget(self._check_cs)
        replace_layout = QHBoxLayout()
        self._line_replace = QLineEdit()
        replace_layout.addWidget(self._line_replace)
        btn_replace = QToolButton()
        btn_replace.setText(self.tr("Replace"))
        replace_layout.addWidget(btn_replace)
        btn_replace_all = QToolButton()
        btn_replace_all.setText(self.tr("Replace all"))
        replace_layout.addWidget(btn_replace_all)

        box.addLayout(find_layout)
        box.addLayout(replace_layout)

        # Conexiones
        self.connect(self._line_search, SIGNAL("textEdited(QString)"),
                     self._find)
        self.connect(btn_replace, SIGNAL("clicked()"), self._replace)
        self.connect(btn_replace_all, SIGNAL("clicked()"), self._replace_all)
        self.connect(self._check_cs, SIGNAL("stateChanged(int)"),
                     self._state_change)
        self.connect(btn_back, SIGNAL("clicked()"), self._find_previous)
        self.connect(btn_forward, SIGNAL("clicked()"), self._find_next)

    def _find(self):
        if not self.word:
            return
        editor_container = Edis.get_component("principal")
        weditor = editor_container.get_active_editor()
        found = weditor.findFirst(self.word, False, self._cs, False, False,
                                  True, 0, 0, True)
        if self.word:
            self._line_search.update(found)
        weditor.hilo_ocurrencias.buscar(self.word, weditor.text())

    def _find_next(self):
        editor_container = Edis.get_component("principal")
        weditor = editor_container.get_active_editor()
        weditor.findFirst(self.word, False, False, False, True,
                          True, -1, -1, True)

    def _find_previous(self):
        editor_container = Edis.get_component("principal")
        weditor = editor_container.get_active_editor()
        weditor.findFirst(self.word, False, False, False, True,
                          False, -1, -1, True)
        weditor.findNext()

    def _replace(self):
        if not self.word_replace:
            return
        editor_container = Edis.get_component("principal")
        weditor = editor_container.get_active_editor()
        if weditor.hasSelectedText():
            weditor.replace(self.word_replace)
            self._find_next()

    def _replace_all(self):
        editor_container = Edis.get_component("principal")
        weditor = editor_container.get_active_editor()
        found = weditor.findFirst(self.word, False, False, False, False,
                                  True, 0, 0, True)
        while found:
            weditor.replace(self.word_replace)
            found = weditor.findNext()

    def _state_change(self, value):
        if value == 2:
            self._cs = True
        else:
            self._cs = False
        self._find()

    @property
    def word(self):
        return self._line_search.text()

    @property
    def word_replace(self):
        return self._line_replace.text()

    def showEvent(self, event):
        super(ReplaceWidget, self).showEvent(event)
        self._line_search.setFocus()