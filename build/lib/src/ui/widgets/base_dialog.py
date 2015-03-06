# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QDialog

from PyQt4.QtCore import (
    Qt,
    #QPoint
    )


class BaseDialog(QDialog):

    """ Base para popup dialog en la esquina superior derecha """

    def __init__(self, weditor):
        super(BaseDialog, self).__init__(weditor)
        self._weditor = weditor
        self.line = None
        # Popup
        self.setWindowFlags(Qt.Popup)
        # Posición
        self.qpoint = weditor.rect().topRight()
        self.global_point = weditor.mapToGlobal(self.qpoint)

    def showEvent(self, event):
        super(BaseDialog, self).showEvent(event)
        self.line.setFocus()