#-*- coding: utf-8 -*-

""" Manejo de archivos """

import os

from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import QFile
from PyQt4.QtCore import QTextStream


def _nombreBase(nombre_de_archivo):
    """ Se retorna el nombre del archivo con la extensión, sin la ruta """

    if nombre_de_archivo.endswith(os.path.sep):
        nombre_de_archivo = nombre_de_archivo[:-1]

    return os.path.basename(nombre_de_archivo)


def leer_contenido_de_archivo(archivo):
    """ Intenta abrir y leer el contenido del archivo, lo retorna en caso de
    éxito, de lo contrario se retora un string vacío  """
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()

        return contenido

    except:
        return ""


def escribir_archivo(nombre_de_archivo, contenido):
    """ Se escribe en el archivo, si el nombre no tiene extension se agrega .c
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
    return os.access(archivo, os.W_OK)