# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import unittest

from src.managers import file_manager


class FileManagerTestCase(unittest.TestCase):

    def setUp(self):
        self._filename = os.path.join(os.path.dirname(__file__),
                                      "c_files", "for_test.c")

    def test_get_file_size(self):
        size = 87  # bytes
        self.assertEqual(size, file_manager.get_file_size(self._filename))


if __name__ == "__main__":
    unittest.main()
