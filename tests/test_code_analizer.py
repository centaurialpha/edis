# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os

from src.tools.ctags import ctags


class CodeAnalizerTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__),
                                     "c_files", "for_ctags.c")

    def test_parse_symbols(self):
        symbols_expected = {
            'functions': {'7': 'main'},
            'structs': {'3': 'ufo'},
            'members': {'name': ('4', 'ufo')},
            'globals': {'UFO': '5'}
            }
        symbols, _ = ctags.get_symbols(self.filename)
        self.assertEqual(symbols, symbols_expected)

    def test_parse_symbols_combo(self):
        symbols_expected = {
            7: ('main( int argc, char** argv )', 'function'),
            3: ('ufo', 'struct')
            }
        _, symbols_combo = ctags.get_symbols(self.filename)
        self.assertEqual(symbols_combo, symbols_expected)

if __name__ == "__main__":
    unittest.main()
