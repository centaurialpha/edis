# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Manejo de archivos """

import os

from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import (
    QFile,
    QTextStream,
    QIODevice
    )


def leer_contenido_de_archivo(archivo):
    """ Intenta abrir y leer el contenido del archivo, lo retorna en caso de
    éxito, de lo contrario se retora un string vacío  """

    try:
        filename = QFile(archivo)
        if not filename.open(QIODevice.ReadOnly | QIODevice.Text):
            return False
        stream = QTextStream(filename)
        data = str(stream.readAll())
        return data
    except IOError:
        raise


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