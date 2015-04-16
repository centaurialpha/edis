# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

#import unittest
#from tests import base_gui
#from PyQt4.QtTest import QTest
#from PyQt4.QtCore import Qt


#class MinimapTestCase(base_gui.BaseGUI):

    #def setUp(self):
        #super(MinimapTestCase, self).setUp()
        #QTest.keyPress(self.edis, Qt.Key_N, Qt.ControlModifier)
        #self.editor_container = self.edis.get_component("principal")

    #def test_minimap(self):
        #editor = self.editor_container.get_active_editor()
        #QTest.keyClicks(editor, "This is a test")
        #self.wait()
        #QTest.keyPress(editor, Qt.Key_Return)
        #QTest.keyClicks(editor, "Lalalalaal la   lalal   lslsksi")
        #self.wait()
        #minimap = getattr(editor, 'minimap')
        #editor_text = editor.text()
        #minimap_text = minimap.text()
        #self.assertEqual(editor_text, minimap_text)


#if __name__ == "__main__":
    #unittest.main()