# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import unittest

from src.helpers import file_manager


class FileManagerTestCase(unittest.TestCase):

    def setUp(self):
        self._filename = os.path.join(os.path.dirname(__file__),
                                  "c_files", "for_test.c")

    def test_read_file(self):
        content = "#include <stdio.h>\n/* qwertyuiopasdfghjklñzxcvbnm */\n" \
            "int main( void ) {\n    return 0;\n}\n"

        self.assertEqual(content, file_manager.get_file_content(self._filename))


if __name__ == "__main__":
    unittest.main()