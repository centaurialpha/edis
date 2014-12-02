# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Manejo de archivos """

import os
# lint:disable
try:
    import json
except ImportError:
    import simplejson as json
# lint:enable

from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import (
    QFile,
    QTextStream,
    QIODevice
    )

from src import recursos


def _nombreBase(nombre_de_archivo):
    """ Se retorna el nombre del archivo con la extensión, sin la ruta """

    if nombre_de_archivo.endswith(os.path.sep):
        nombre_de_archivo = nombre_de_archivo[:-1]

    return os.path.basename(nombre_de_archivo)


def nombre_de_archivo(nombre_de_archivo):
    """ Devuelve el nombre de un archivo, sin extensión. """
    modulo = os.path.basename(nombre_de_archivo)
    return (os.path.splitext(modulo)[0])


def devolver_carpeta(nombre_de_archivo):
    return os.path.dirname(nombre_de_archivo)


def archivos_desde_carpeta(carpeta, extension):
    """ Devuelve una lista con todos los archivos de @carpeta con extensión
    @extension. """

    try:
        archivo_extension = os.listdir(carpeta)
    except:
        archivo_extension = []
    archivo_extension = [f for f in archivo_extension if f.endswith(extension)]
    return archivo_extension


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


def permiso_de_escritura(archivo):
    """ Retorna True si el archivo tiene permisos de escritura o False
    en caso contrario. """

    return os.access(archivo, os.W_OK)


def crear_path(*args):
    return os.path.join(*args)


def archivo_existente(path, nombre_archivo=''):
    """ Devuelve True si el archivo se encuentra en @path y False en caso
    contrario. """

    if nombre_archivo:
        path = os.path.join(path, nombre_archivo)
    return os.path.isfile(path)


def guardar_tema_editor(nombre_archivo, tema):
    archivo = open(nombre_archivo, mode='w')
    json.dump(tema, archivo, indent=2)
    archivo.close()


def cargar_temas_editor():
    archivos = os.listdir(recursos.TEMAS_GUARDADOS)
    temas = {}
    for tema in archivos:
        if tema.endswith('.color'):
            estructura = None
            nombre_archivo = os.path.join(recursos.TEMAS_GUARDADOS, tema)
            leer = open(nombre_archivo, 'r')
            estructura = json.load(leer)
            leer.close()
            nombre = unicode(tema[:-6])
            temas[nombre] = estructura

    return temas