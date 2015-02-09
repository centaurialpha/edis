# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Manejo de archivos """

import os

from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import (
    QFile,
    QTextStream
    )
from src.helpers.exceptions import EdisIOException


def get_file_content(archivo):
    """ Lee el contenido de @archivo y lo retorna """

    try:
        with open(archivo, mode='r') as filename:
            content = filename.read()
    except IOError as error:
        raise EdisIOException(error)
    return content


def devolver_tam_archivo(archivo):
    """ Retorna el tamaño del archivo en bytes. """

    tam = QFile(archivo).size()
    return tam


def escribir_archivo(nombre_de_archivo, contenido):
    """ Se escribe en el archivo, si el nombre no tiene extensión se agrega .c
    """

    extension = (os.path.splitext(nombre_de_archivo)[-1])[1:]
    if not extension:
        nombre_de_archivo += '.c'

    try:
        f = QFile(nombre_de_archivo)
        if not f.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning("Guardar", "No se escribio en %s: %s" % (
                nombre_de_archivo, f.errorString()))

            return False

        flujo = QTextStream(f)
        encode_flujo = flujo.codec().fromUnicode(contenido)
        f.write(encode_flujo)
        f.flush()
        f.close()

    except:
        pass

    return os.path.abspath(nombre_de_archivo)