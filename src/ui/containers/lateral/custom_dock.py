# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QDockWidget

from PyQt4.QtCore import Qt


class CustomDock(QDockWidget):

    def __init__(self):
        QDockWidget.__init__(self)
        # Siempre undock/redock a la izquierda
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setMaximumWidth(356)