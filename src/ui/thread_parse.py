# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
import os
from subprocess import Popen, PIPE

from PyQt4.QtCore import (
    SIGNAL,
    QThread
    )

from src.tools.pycparser import c_parser
from src.tools import code_analizer
from src import paths
from src.helpers import (
    logger,
    settings
    )

path = os.path.join(paths.PATH, "tools", "pycparser")
# Fake libc
fake_libc = '-I' + os.path.join(path, "fake_libc_include")
# CPP path
cpp_path = os.path.join(path, "cpp.exe") if sys.platform == 'win32' else 'cpp'
# Logger
log = logger.edis_logger.get_logger(__name__)
ERROR = log.error


class Thread(QThread):

    """ Este hilo evita que la aplicación se "tilde" al realizar el
        parseo con cpp, quizás en sistemas no Unix el widget de símbolos
        tarde un cierto tiempo en actualizarse, es cuando el hilo está
        trabajando.

     """

    def run(self):
        symbols, symbols_combo = {}, {}
        error = False
        text = self.process()
        parser = c_parser.CParser()
        try:
            ast = parser.parse(text, self._filename)
        except Exception as reason:
            error = True
            ERROR('El código fuente tiene errores de sintáxis: %s', reason)
        if not error:
            visitor = code_analizer.NodeVisitor()
            visitor.visit(ast)
            if visitor.functions:
                symbols['functions'] = visitor.functions
            if visitor.structs:
                symbols['structs'] = visitor.structs
            if visitor.enums:
                symbols['enums'] = visitor.enums
            symbols_combo = visitor.symbols_combo
        self.emit(SIGNAL("symbols(PyQt_PyObject, PyQt_PyObject)"),
                  symbols, symbols_combo)

    def process(self):
        """ Corre el comando cpp """

        command = [cpp_path] + [fake_libc] + [self._filename]
        if not settings.IS_LINUX:
            # Flag para ocultar la consola
            CREATE_NO_WINDOW = 0x08000000
            process = Popen(command,
                            stdout=PIPE,
                            universal_newlines=True,
                            creationflags=CREATE_NO_WINDOW)
        else:
            process = Popen(command,
                            stdout=PIPE,
                            universal_newlines=True)
        text, _ = process.communicate()
        return text

    def parse(self, filename):
        self._filename = filename
        if not self.isRunning():
            self.start()
        else:
            self.wait()
            self.start()
