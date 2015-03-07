# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os

from src.tools import code_analizer

CODE = """
#include <stdio.h>
struct ufo {
    int a;
};
//testing
void main( void ) {
    return;
}
"""


class CodeAnalizerTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__),
                                     "c_files", "for_test.c")

    def test_parse_symbols(self):
        pass

    def test_sanitize_source_coude(self):
        expected = "\n\nstruct ufo {\n    int a;\n};\n\nvoid main( void ) " \
                   "{\n    return;\n}\n"
        self.assertEqual(expected, code_analizer.sanitize_source_code(CODE))

if __name__ == "__main__":
    unittest.main()