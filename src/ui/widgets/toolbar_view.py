# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtGui import (
    QToolBar,
    QWidget,
    QSizePolicy
    )


from src import recursos
from src.ui.widgets.creador_widget import create_button


class TopToolBar(QToolBar):

    def __init__(self, edis):
        QToolBar.__init__(self)
        self.edis = edis
        self.setMovable(False)
        self.lateral_button = create_button(self,
            icon=recursos.ICONOS['lateral'], toggled=self._show_hide_lateral)
        self.lateral_button.setCheckable(True)
        self.lateral_button.setChecked(True)
        self.output_button = create_button(self,
            icon=recursos.ICONOS['output'], toggled=self._show_hide_output)
        self.output_button.setCheckable(True)
        self.output_button.setChecked(True)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.addWidget(spacer)
        self.addWidget(self.lateral_button)
        self.addWidget(self.output_button)

    def _show_hide_lateral(self):
        self.edis.widget_Central.show_hide_lateral()

    def _show_hide_output(self):
        self.edis.widget_Central.show_hide_output()