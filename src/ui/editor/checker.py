# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtCore import QThread

from src.tools import style_checker


class Checker(QThread):

    def __init__(self, editor):
        super(Checker, self).__init__()
        self._weditor = editor
        self.data = {}

    def run(self):
        data = style_checker.run_checker(self._source)
        for line in data:
            nline, message = line.split(':')
            self.data[nline] = message

    def start_checker(self):
        self._source = self._weditor.texto
        self.data = {}
        self.start()