# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os

from src.tools import code_analizer
from src.tools.pycparser import c_parser

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

CODE2 = """
struct ufo {
    int a;
};

int foo( int a, int b ) {
    return 1;
}

void main( void ) {
    return;
}
"""


class CodeAnalizerTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__),
                                     "c_files", "for_test.c")
        self.visitor = code_analizer.NodeVisitor()

    def test_parse_symbols(self):
        symbols_expected = {
            2: ('ufo', 'struct'),
            6: ('foo(a, b)', 'function'),
            10: ('main()', 'function')
            }
        parser = c_parser.CParser()
        ast = parser.parse(CODE2)
        self.visitor.visit(ast)
        self.assertEqual(symbols_expected, self.visitor.symbols_combo)

    def test_sanitize_source_coude(self):
        expected = "\n\nstruct ufo {\n    int a;\n};\n\nvoid main( void ) " \
                   "{\n    return;\n}\n"
        self.assertEqual(expected, code_analizer.sanitize_source_code(CODE))

if __name__ == "__main__":
    unittest.main()
