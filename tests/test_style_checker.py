# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os

from src.tools import style_checker


class StyleCheckerTestCase(unittest.TestCase):

    def setUp(self):
        self.c_file = os.path.join(os.path.dirname(__file__),
                                   "c_files", "for_check.c")

    def test_checkers(self):
        with open(self.c_file, mode='r') as f:
            content = f.read()
        result = style_checker.run_checker(content)
        paren_curly_space = int(result[0][:1])
        max_line = int(result[1][:1])
        coma_space = int(result[4][:1])
        operator_space = int(result[5][:1])
        comment_open_space = int(result[2][:1])
        comment_close_space = int(result[3][:1])
        self.assertEqual(paren_curly_space, 3)
        self.assertEqual(max_line, 4)
        self.assertEqual(coma_space, 5)
        self.assertEqual(operator_space, 7)
        self.assertEqual(comment_open_space, 4)
        self.assertEqual(comment_close_space, 4)

if __name__ == "__main__":
    unittest.main()