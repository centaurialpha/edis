# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from src.ui.widgets import tool_button
from src.ui.main import EDIS


class DockManager(QObject):

    def __init__(self):
        super(DockManager, self).__init__()

        EDIS.cargar_componente("dock", self)


dock_manager = DockManager()