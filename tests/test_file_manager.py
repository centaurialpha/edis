# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import unittest
import tempfile

from src.helpers import file_manager
from src.helpers.exceptions import EdisIOException


class FileManagerTestCase(unittest.TestCase):

    def setUp(self):
        self._filename = os.path.join(os.path.dirname(__file__),
                                  "c_files", "for_test.c")

    def test_read_file(self):
        content = "#include <stdio.h>\n/* qwertyuiopasdfghjklñzxcvbnm */\n" \
            "int main( void ) {\n    return 0\n}"

        self.assertEqual(content, file_manager.get_file_content(self._filename))

    def test_exception_read_file(self):
        fake_filename = "/home/gabo/fake.c"  # No existe
        self.assertRaises(EdisIOException,
            lambda: file_manager.get_file_content(fake_filename))

    def test_get_file_size(self):
        size = 87  # bytes
        self.assertEqual(size, file_manager.get_file_size(self._filename))

    def test_write_file(self):
        temp_filename = tempfile.mkstemp()[1]
        content = "Testing write file function. íñÑó"
        temp_filename = file_manager.write_file(temp_filename, content)
        _file = open(temp_filename)
        try:
            self.assertEqual(_file.read(), "Testing write file function. íñÑó")
        finally:
            _file.close()
            os.remove(temp_filename)


if __name__ == "__main__":
    unittest.main()