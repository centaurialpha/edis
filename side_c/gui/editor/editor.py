#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit


class Editor(QPlainTextEdit):

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)


def crear_editor(nombre_archivo=''):
    editor = Editor(nombre_archivo)

    return editor