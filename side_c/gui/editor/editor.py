#-*- coding: utf-8 -*-
import sys

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFontMetricsF
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QFont

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QRect

from PyQt4.Qt import QVariant
from PyQt4.Qt import QTextFormat

from side_c import recursos
from side_c import configuraciones
from side_c.gui.editor import widget_numero_lineas
from side_c.gui.editor.highlighter import Highlighter

# Fuente por defecto
FUENTE = QFont('Monospace', 11)

# Si estamos en Windows
if sys.platform == "win32":
    FUENTE = QFont('Courier', 12)


class Editor(QPlainTextEdit):

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)

        font_metrics = QFontMetricsF(self.document().defaultFont())
        self.posicion_margen = font_metrics.width('#') * 80
        self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)

        #self._encoding = None
        #self.indentacion_ = 4
        self.useTabs = True
        self.texto_modificado = False
        self.nuevo_archivo = True
        # Carga tema de editor
        self.estilo_editor()
        self.setFont(FUENTE)

        Highlighter(self.document())

        # Highlighting
        self.resaltar_linea_actual()

        self.connect(self, SIGNAL("cursorPositionChanged()"),
            self.resaltar_linea_actual)
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
            self.resaltar_linea_actual()

    def resizeEvent(self, event):
        """ Redimensiona la altura del widget. """

        QPlainTextEdit.resizeEvent(self, event)
        self.widget_num_lineas.setFixedHeight(self.height())

    def paintEvent(self, event):
        """ Evento que dibuja el margen de línea."""

        QPlainTextEdit.paintEvent(self, event)
        pintar = QPainter()
        pintar.begin(self.viewport())
        pintar.setPen(QColor(recursos.COLOR_EDITOR['margen-linea']))
        offset = self.contentOffset()
        ancho = self.viewport().width() - (self.posicion_margen + offset.x())
        rect = QRect(self.posicion_margen + offset.x(), 1,
            ancho + 1, self.viewport().height() + 3)
        fondo = QColor(recursos.COLOR_EDITOR['fondo-margen'])
        fondo.setAlpha(recursos.COLOR_EDITOR['opacidad'])
        pintar.fillRect(rect, fondo)
        pintar.drawRect(rect)
        pintar.drawLine(self.posicion_margen + offset.x(), 0,
            self.posicion_margen + offset.x(), self.viewport().height())
        pintar.end()

    def posicion_cursor(self, posicion):
        if self.document().characterCount() >= posicion:
            c = self.textCursor()
            c.setPosition(posicion)
            self.setTextCursor(c)

    def resaltar_linea_actual(self):
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

    def devolver_texto(self):
        """ Retorna todo el contenido del editor """

        return self.toPlainText()

    def actualizar_margen_linea(self, fuente=None):
        if not fuente:
            fuente = self.document().defaultFont()
        if "ForceIntegerMetrics" in dir(QFont):
            self.document().defaultFont().setStyleStrategy(
                QFont.ForceIntegerMetrics)

        f_metrics = QFontMetricsF(self.document().defaultFont())
        if (f_metrics.width("#") * configuraciones.MARGEN) == \
        (f_metrics.width(" ") * configuraciones.MARGEN):
            self.posicion_margen = f_metrics.width('#') * \
               configuraciones.MARGEN
        else:
            c_width = f_metrics.averageCharWidth()
            self.posicion_margen = c_width * configuraciones.MARGEN


def crear_editor(nombre_archivo=''):
    editor = Editor(nombre_archivo)

    return editor