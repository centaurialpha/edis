#-*- coding: utf-8 -*-

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QColor

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from PyQt4.Qt import QVariant
from PyQt4.Qt import QTextFormat

from side_c import recursos
from side_c.gui.editor import widget_numero_lineas


class Editor(QPlainTextEdit):

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)

        self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)
        self.estilo_editor()
        self.highlight()

        self.connect(self, SIGNAL("cursorPositionChanged()"),
            self.highlight)
        self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
            self.widget_num_lineas.actualizar_area)

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

    def resizeEvent(self, event):
        """ Redimensiona la altura del widget. """

        QPlainTextEdit.resizeEvent(self, event)
        self.widget_num_lineas.setFixedHeight(self.height())

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