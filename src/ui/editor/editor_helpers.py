# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtCore import (
    pyqtSignal,
    QThread
    )


class SearchThread(QThread):
    """ Éste hilo busca ocurrencias de una palabra en el código fuente """

    foundWords = pyqtSignal("PyQt_PyObject")

    def run(self):
        found_list = []
        found_generator = self.ffind_with_lines(self._text, self._word)
        for i in found_generator:
            found_list.append([i[2], i[0], i[1]])

        self.foundWords.emit(found_list)

    def ffind_with_lines(self, text, word):
        for line_number, line in enumerate(text.splitlines()):
            for index, end in self.ffind(line, word):
                yield index, end, line_number

    def ffind(self, text, word):
        i = 0
        while True:
            i = text.find(word, i)
            if i == -1:
                return
            end = i + len(word)
            yield i, end
            i += len(word)

    def find(self, word, source):
        self._text = source
        self._word = word

        # Run!
        self.start()