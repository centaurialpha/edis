#-*- coding: utf-8 -*-

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
from side_c.nucleo import configuraciones
from side_c.interfaz.editor import widget_numero_lineas
from side_c.interfaz.editor.highlighter import Highlighter
#from side_c.interfaz.editor import acciones_


class Editor(QPlainTextEdit):
    """ Editor """

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)

        font_metrics = QFontMetricsF(self.document().defaultFont())
        self.posicion_margen = font_metrics.width('#') * 80
        self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)

        self.indentacion = 4
        self.texto_modificado = False
        self.nuevo_archivo = True
        self.guardado_actualmente = False
        # Carga el tema de editor
        self.estilo_editor()

        # Carga el tipo de letra
        self._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        # Resaltado de sintáxis
        Highlighter(self.document())

        # Resaltado en posición del cursor
        self.resaltar_linea_actual()

        self.presionadoAntes = {Qt.Key_Tab: self._indentar}
        self.presionadoDespues = {Qt.Key_Enter: self._auto_indentar,
        Qt.Key_Return: self._auto_indentar}

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
        if configuraciones.MOSTRAR_MARGEN:
            pintar = QPainter()
            pintar.begin(self.viewport())
            pintar.setPen(QColor(recursos.COLOR_EDITOR['margen-linea']))
            offset = self.contentOffset()
            ancho = self.viewport().width() - (self.posicion_margen +
                offset.x())
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

    def keyPressEvent(self, evento):
        #if evento.key() == Qt.Key_Tab:
            #self._indentar(evento)
        #elif evento.key() == Qt.Key_Return:
            #self._auto_indentar(evento)
        #else:
            #QPlainTextEdit.keyPressEvent(self, evento)
        if self.presionadoAntes.get(evento.key(), lambda a: False)(evento):
            self.emit(SIGNAL("keyPressEvent(QEvent)"), evento)
            return
        QPlainTextEdit.keyPressEvent(self, evento)

        self.presionadoDespues.get(evento.key(), lambda a: False)(evento)
        self.emit(SIGNAL("keyPressEvent(QEvent)"), evento)

    def _indentar(self, evento):
        """ Inserta 4 espacios si se preciosa la tecla Tab """

        self.textCursor().insertText(' ' * self.indentacion)
        return True

    def _auto_indentar(self, evento):
        """ Inserta automáticamente 4 espacios después de presionar Enter,
        previamente escrito '{' """

        texto = self.textCursor().block().previous().text()
        espacios = self.__indentacion(texto, self.indentacion)
        self.textCursor().insertText(espacios)

        cursor = self.textCursor()
        cursor.setPosition(cursor.position())
        self.setTextCursor(cursor)

    def devolver_texto(self):
        """ Retorna todo el contenido del editor """

        return self.toPlainText()

    def _cargar_fuente(self, fuente_=configuraciones.FUENTE,
        tam=configuraciones.TAM_FUENTE):

            fuente = QFont(fuente_, tam)
            self.document().setDefaultFont(fuente)
            self.actualizar_margen_linea(fuente)

    def zoom_mas(self):
        fuente = self.document().defaultFont()
        tam = fuente.pointSize()

        if tam < configuraciones.FUENTE_MAX_TAM:
            tam += 1
            fuente.setPointSize(tam)

        self.setFont(fuente)
        self.actualizar_margen_linea(fuente)

    def zoom_menos(self):
        fuente = self.document().defaultFont()
        tam = fuente.pointSize()

        if tam > configuraciones.FUENTE_MIN_TAM:
            tam -= 1
            fuente.setPointSize(tam)

        self.setFont(fuente)
        self.actualizar_margen_linea(fuente)

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

    def _guardado(self):
        self.nuevo_archivo = False
        self.texto_modificado = False
        self.document().setModified(self.texto_modificado)

    def __indentacion(self, linea, ind):
        import re
        patronInd = re.compile('^\s+')
        indentacion = ''

        if len(linea) > 0 and linea[-1] == '{':
            indentacion = ' ' * ind
        espacio = patronInd.match(linea)
        if espacio is not None:
            return espacio.group() + indentacion

        return indentacion


def crear_editor(nombre_archivo=''):
    editor = Editor(nombre_archivo)

    return editor