# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os
from src.ui.main import Edis
from PyQt4.QtTest import QTest
from . import qApp
from src import paths


class BaseGUI(unittest.TestCase):

    def setUp(self):
        self.app = qApp
        style = os.path.join(paths.PATH, "extras", "theme", "edark.qss")
        with open(style, 'r') as f:
            self.app.setStyleSheet(f.read())
        self.edis = Edis()
        self.edis.show()
        QTest.qWaitForWindowShown(self.edis)

    def wait(self, time=500):
        QTest.qWait(time)

    def tearDown(self):
        del self.app