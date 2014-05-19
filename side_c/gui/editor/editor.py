#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit


class Editor(QPlainTextEdit):

    def __init__(self):
        super(Editor, self).__init__()

    def crear_editor(self):
        editor = Editor()

        return editor