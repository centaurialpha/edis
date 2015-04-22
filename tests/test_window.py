# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

#import unittest

#from PyQt4.QtTest import QTest
#from PyQt4.QtCore import Qt
#from tests import base_gui


#class WindowTestCase(base_gui.BaseGUI):

    #def test_show_fullscreen(self):
        #pass

    #def test_show_hide_lateral(self):
        #lateral = self.edis.get_component("tab_container")
        ## Show lateral
        #QTest.keyPress(self.edis, Qt.Key_F6)
        #isVisible = lateral.isVisible()
        #self.assertEqual(isVisible, True)
        ## Hide lateral
        #QTest.keyPress(self.edis, Qt.Key_F6)
        #isVisible = lateral.isVisible()
        #self.assertEqual(isVisible, False)

    #def test_show_hide_output(self):
        #output = self.edis.get_component("output")
        ## Show
        #QTest.keyPress(self.edis, Qt.Key_F7)
        #self.assertEqual(output.isVisible(), True)
        ## Hide
        #QTest.keyPress(self.edis, Qt.Key_F7)
        #self.assertEqual(output.isVisible(), False)

    #def test_show_hide_toolbar(self):
        #pass

    #def test_show_hide_dev_mode(self):
        #widgets = ["tab_container", "status_bar", "output"]
        ## Hide all
        #QTest.keyPress(self.edis, Qt.Key_F11)
        #for widget in widgets:
            #visible = self.edis.get_component(widget).isVisible()
            #self.assertEqual(visible, False)


#if __name__ == "__main__":
    #unittest.main()