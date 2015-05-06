# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtCore import (
    QObject,
    QFile,
    QIODevice,
    QTextStream,
    QFileSystemWatcher,
    SIGNAL
    )

from src.core import (
    exceptions,
    logger
    )

log = logger.get_logger(__name__)
DEBUG = log.debug


class EdisFile(QObject):
    """ Representación de un objeto archivo """

    def __init__(self, filename=''):
        QObject.__init__(self)
        self._is_new = True
        if not filename:
            self._filename = "Untitled"
        else:
            self._filename = filename
            self._is_new = False
        self._last_modification = None
        self._system_watcher = None

    @property
    def filename(self):
        return self._filename

    @property
    def is_new(self):
        return self._is_new

    def read(self):
        """ Itenta leer el contenido del archivo, si ocurre un error se lanza
        una excepción.
        """

        try:
            with open(self.filename, mode='r') as f:
                content = f.read()
            return content
        except IOError as reason:
            raise exceptions.EdisIOError(reason)

    def write(self, content, new_filename=''):
        """ Escribe los datos en el archivo """

        DEBUG("Saving file...")
        # Por defecto, si el archivo no tiene extensión se agrega .c
        ext = os.path.splitext(new_filename)
        if not ext[-1]:
            new_filename += '.c'
        if self.is_new:
            self._filename = new_filename
            self._is_new = False
        _file = QFile(self.filename)
        if not _file.open(QIODevice.WriteOnly | QIODevice.Truncate):
            raise exceptions.EdisIOError
        out_file = QTextStream(_file)
        out_file << content
        self.run_system_watcher()

    def run_system_watcher(self):
        """ Inicializa el control de monitoreo para modificaciones """

        if self._system_watcher is None:
            self._system_watcher = QFileSystemWatcher()
            self.connect(self._system_watcher,
                         SIGNAL("fileChanged(const QString&)"),
                         self._on_file_changed)
        self._last_modification = os.lstat(self.filename).st_mtime
        self._system_watcher.addPath(self.filename)
        DEBUG("Watching {0}".format(self.filename))

    def stop_system_watcher(self):
        if self._system_watcher is not None:
            self._system_watcher.removePath(self.filename)
            DEBUG("Stoping watching {0}".format(self.filename))

    def _on_file_changed(self, filename):
        mtime = os.lstat(filename).st_mtime
        if mtime != self._last_modification:
            # Actualizo la última modificación
            self._last_modification = mtime
            self.emit(SIGNAL("fileChanged(PyQt_PyObject)"), self)