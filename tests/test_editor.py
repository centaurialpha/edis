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


class EditorTestCase(base_gui.BaseGUI):

    def setUp(self):
        super(EditorTestCase, self).setUp()
        QTest.keyPress(self.edis, Qt.Key_N, Qt.ControlModifier)
        self.editor_container = self.edis.get_component("principal")
        self._filename = os.path.join(os.path.dirname(__file__),
                                      "c_files", "for_test.c")

    def test_1(self):
        editor = self.editor_container.get_active_editor()
        QTest.keyClicks(editor, "lalsdkalksdas jdhaksjdh")
        # Seleccionar
        QTest.keyPress(self.edis, Qt.Key_A, Qt.ControlModifier)
        self.wait()
        expected = "lalsdkalksdas jdhaksjdh"
        self.assertEqual(editor.selectedText(), expected)
        # Cortar
        QTest.keyPress(self.edis, Qt.Key_X, Qt.ControlModifier)
        self.wait()
        expected = ""
        self.assertEqual(editor.selectedText(), expected)
        # Pegar
        QTest.keyPress(self.edis, Qt.Key_V, Qt.ControlModifier)
        QTest.keyPress(self.edis, Qt.Key_V, Qt.ControlModifier)
        self.wait()
        expected = "lalsdkalksdas jdhaksjdhlalsdkalksdas jdhaksjdh"
        self.assertEqual(editor.text(), expected)
        # Deshacer
        QTest.keyPress(self.edis, Qt.Key_Z, Qt.ControlModifier)
        self.wait()
        expected = "lalsdkalksdas jdhaksjdh"
        self.assertEqual(editor.text(), expected)

    def test_open_file(self):
        self.editor_container.open_file(self._filename)
        content = self.editor_container.get_active_editor().text()
        _file = open(self._filename)
        self.assertEqual(content, _file.read())
        _file.close()

    def test_find(self):
        editor = self.editor_container.get_active_editor()
        QTest.keyClicks(editor, "chavo Chavo CHAVO ChAVVO 8")
        QTest.keyPress(self.edis, Qt.Key_F, Qt.ControlModifier)
        QTest.keyClicks(None, "chavo")
        self.assertEqual(editor.selectedText(), "chavo")

    def test_go_to_line(self):
        editor = self.editor_container.get_active_editor()
        for i in range(10):
            QTest.keyPress(editor, Qt.Key_Enter)
        QTest.keyPress(self.edis, Qt.Key_J, Qt.ControlModifier)
        QTest.keyClicks(None, "6")
        QTest.keyPress(None, Qt.Key_Enter)
        # line comienza en 0
        line, _ = editor.getCursorPosition()
        self.assertEqual(line + 1, 6)


if __name__ == "__main__":
    unittest.main()