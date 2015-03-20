# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest

from PyQt4.QtGui import QApplication

from src.ui.dialogs.preferences import (
    editor_configuration,
    general_configuration
    )


class PreferencesTestCase(unittest.TestCase):

    def setUp(self):
        # GUI
        self.app = QApplication([])
        self.editor_preferences = editor_configuration.EditorConfiguration()
        self.gral_preferences = general_configuration.GeneralConfiguration(
            None)

    def setFormToZero(self):
        self.editor_preferences.slider_margin.setValue(0)
        self.editor_preferences.slider_indentation.setValue(0)

    def test_default_values(self):
        self.assertEqual(self.gral_preferences.check_on_start.isChecked(),
                         True)
        self.assertEqual(self.gral_preferences.check_on_exit.isChecked(),
                         True)
        self.assertEqual(self.gral_preferences.check_geometry.isChecked(),
                         True)
        self.assertEqual(self.gral_preferences.check_updates.isChecked(),
                         True)
        self.assertEqual(self.editor_preferences.check_margin.isChecked(),
                         True)
        self.assertEqual(self.editor_preferences.slider_margin.value(), 79)
        self.assertEqual(self.editor_preferences.check_indentation.isChecked(),
                         True)
        self.assertEqual(self.editor_preferences.slider_indentation.value(), 4)
        self.assertEqual(self.editor_preferences.check_guides.isChecked(),
                         False)
        self.assertEqual(
            self.editor_preferences.check_style_checker.isChecked(), True)
        self.assertEqual(self.editor_preferences.check_minimap.isChecked(),
                         False)

    def tearDown(self):
        del self.app

if __name__ == "__main__":
    unittest.main()
