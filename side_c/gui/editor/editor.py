#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.Qt import QVariant
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush
from PyQt4.QtCore import Qt
from PyQt4.Qt import QTextFormat
from side_c import recursos


class Editor(QPlainTextEdit):

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)

        self.estilo_editor()
        self.highlight()

    def estilo_editor(self):
        """ Aplica estilos de colores al editor """

        tema_editor = 'QPlainTextEdit {color: %s; background-color: %s;}' \
        % (recursos.COLOR_EDITOR['texto'], recursos.COLOR_EDITOR['fondo'])

        self.setStyleSheet(tema_editor)

    def mouseReleaseEvent(self, event):
        """ Actualiza highlight según un evento del mouse. """

        QPlainTextEdit.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.highlight()

    def highlight(self):
        """ Pinta la linea actual en donde está posicionado el cursor. """

        seleccion = QTextEdit.ExtraSelection()
        color = QColor(recursos.COLOR_EDITOR['linea-actual'])
        color.setAlpha(40)
        seleccion.format.setBackground(color)
        seleccion.format.setProperty(
            QTextFormat.FullWidthSelection, QVariant(True))
        seleccion.cursor = self.textCursor()
        seleccion.cursor.clearSelection()

        self.setExtraSelections([seleccion])


def crear_editor(nombre_archivo=''):
    editor = Editor(nombre_archivo)

    return editor