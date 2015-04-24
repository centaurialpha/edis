# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Manejo de archivos """

import os

from PyQt4.QtCore import (
    QFile,
    QIODevice,
    QTextStream
    )

from src.core.exceptions import (
    EdisFileExistsError,
    EdisIOError
    )


def write_file(filename, content):
    _file = QFile(filename)
    if not _file.open(QIODevice.WriteOnly | QIODevice.Truncate):
        raise EdisIOError
    outfile = QTextStream(_file)
    outfile << content
    return filename


def get_file_size(_file):
    """ Retorna el tamaño del archivo en bytes. """

    size = QFile(_file).size()
    return size


def rename_file(old_name, new_name):
    """ Renombra un archivo """

    if os.path.exists(new_name):
        raise EdisFileExistsError(new_name)
    os.rename(old_name, new_name)


def file_exists(filename):
    """ Devuelve True si @filename existe, False en caso contrario """

    return os.path.isfile(filename)


def delete_file(filename):
    """ Borra un archivo """
    pass


def get_basename(filename):
    return os.path.basename(filename)