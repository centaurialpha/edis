# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os
from tests import base_gui
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class StatusBarTestCase(base_gui.BaseGUI):

    def setUp(self):
        super(StatusBarTestCase, self).setUp()
        self.editor_container = self.edis.get_component("principal")
        self.status_bar = self.edis.get_component("status_bar")

    def test_update_status(self):
        filename = os.path.join(os.path.dirname(__file__),
                                "c_files", "for_test.c")
        # Nuevo stack
        QTest.keyPress(self.edis, Qt.Key_N, Qt.ControlModifier)
        status_bar_path = self.status_bar.lbl_archivo.text()
        self.assertEqual(status_bar_path, "Untitled")
        # Open new file
        self.editor_container.open_file(filename)
        # El path ha cambiado
        status_bar_path = self.status_bar.lbl_archivo.text()
        self.assertEqual(status_bar_path, filename)

    def test_update_time(self):
        uptime_widget = self.status_bar.uptime_widget
        current_time = uptime_widget.text().split(':')[1].strip()
        self.assertEqual(current_time, '0min')
        uptime_widget.tiempo = 119
        uptime_widget.update_time()
        current_time = uptime_widget.text().split(':')[1].strip()
        self.assertEqual(current_time, '2hs0min')


if __name__ == "__main__":
    unittest.main()