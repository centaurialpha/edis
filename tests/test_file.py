# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import unittest
import os
import tempfile

from src.core import (
    object_file
    )


class EdisFileTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.join(os.path.dirname(__file__))
        self._filename = os.path.join(current_dir, "c_files", "for_test.c")

    def test_read(self):
        fedis = object_file.EdisFile(self._filename)
        expected = "#include <stdio.h>\n/* qwertyuiopasdfghjklñzxcvbnm */\n" \
                   "int main( void ) {\n    return 0\n}"
        content = fedis.read()
        self.assertEqual(expected, content)

    def test_write(self):
        tmp_file = tempfile.NamedTemporaryFile()
        fedis = object_file.EdisFile(tmp_file.name)
        fedis.write("Testing write file function. íñÑó")
        expected = "Testing write file function. íñÑó"
        with open(tmp_file.name, mode='r') as f:
            self.assertEqual(f.read(), expected)

    def test_is_new_file(self):
        fedis = object_file.EdisFile(self._filename)
        self.assertFalse(fedis.is_new)

    def test_is_not_new_file(self):
        fedis = object_file.EdisFile()
        self.assertTrue(fedis.is_new)


if __name__ == "__main__":
    unittest.main()