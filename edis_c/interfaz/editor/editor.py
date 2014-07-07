#-*- coding: utf-8 -*-

# <Editor.>
# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

import re

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFontMetricsF
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextOption

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QRect

from PyQt4.Qt import QVariant
from PyQt4.Qt import QTextFormat

from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.interfaz.editor import widget_numero_lineas
from edis_c.interfaz.editor.highlighter import Highlighter
from edis_c.interfaz import tabitem
from edis_c.interfaz.editor import minimapa

# Diccionario teclas
TECLA = {
    'TABULACION': Qt.Key_Tab,
    'ENTER': Qt.Key_Return,
    'LLAVE': Qt.Key_BraceLeft,
    'PARENTESIS': Qt.Key_ParenLeft,
    'CORCHETE': Qt.Key_BracketLeft,
    'BACKSPACE': Qt.Key_Backspace
    }


class Editor(QPlainTextEdit, tabitem.TabItem):
    """ Editor """

    def __init__(self, nombre_archivo):
        QPlainTextEdit.__init__(self)
        tabitem.TabItem.__init__(self)

        self.set_flags()
        font_metrics = QFontMetricsF(self.document().defaultFont())
        self.posicion_margen = font_metrics.width('#') * 80
        #self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)

        self.texto_modificado = False
        self.nuevo_archivo = True
        self.patronEsPalabra = re.compile('\w+')
        self.guardado_actualmente = False
        self.widget_num_lineas = None
        self.highlighter = None
        self.minimapa = None
        # Carga el tema de editor
        self.estilo_editor()

        # Carga el tipo de letra
        self._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        # Sidebar
        if configuraciones.SIDEBAR:
            self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)

        # Resaltado de sintáxis
        if self.highlighter is None:
            self.highlighter = Highlighter(self.document())

        # Resaltado en posición del cursor
        self.resaltar_linea_actual()

        self.presionadoAntes = {
            TECLA.get('TABULACION'): self._indentar,
            TECLA.get('BACKSPACE'): self.__tecla_backspace
            }

        self.presionadoDespues = {
            TECLA.get('ENTER'): self._auto_indentar,
            TECLA.get('LLAVE'): self._completar_braces,
            TECLA.get('CORCHETE'): self._completar_braces,
            TECLA.get('PARENTESIS'): self._completar_braces
            }

        self.connect(self, SIGNAL("undoAvailable(bool)"), self._guardado)
        self.connect(self, SIGNAL("cursorPositionChanged()"),
            self.resaltar_linea_actual)
        if self.widget_num_lineas is not None:
            self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                self.widget_num_lineas.actualizar_area)

        # Minimapa
        if configuraciones.MINIMAPA:
            self.minimapa = minimapa.MiniMapa(self)
            self.minimapa.show()
            self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                self.minimapa.actualizar_area_visible)
            self.minimapa.highlighter = Highlighter(self.minimapa.document())

    def set_id(self, id_):
        super(Editor, self).set_id(id_)
        self.minimapa.set_code(self.toPlainText())

    def estilo_editor(self):
        """ Aplica estilos de colores al editor """

        tema_editor = 'QPlainTextEdit {color: %s; background-color: %s;}' \
        % (recursos.COLOR_EDITOR['texto'], recursos.COLOR_EDITOR['fondo'])

        self.setStyleSheet(tema_editor)

    def set_flags(self):
        self.setMouseTracking(True)
        doc = self.document()
        op = QTextOption()
        if configuraciones.MOSTRAR_TABS:
            op.setFlags(QTextOption.ShowTabsAndSpaces)
        doc.setDefaultTextOption(op)
        self.setDocument(doc)

    def mouseReleaseEvent(self, event):
        """ Actualiza highlight según un evento del mouse. """

        QPlainTextEdit.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.resaltar_linea_actual()

    def resizeEvent(self, event):
        """ Redimensiona la altura del widget. """

        QPlainTextEdit.resizeEvent(self, event)
        if self.widget_num_lineas is not None:
            self.widget_num_lineas.setFixedHeight(self.height())
        if self.minimapa:
            self.minimapa.ajustar_()

    def texto_abajo(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        palabra = cursor.selectedText()
        r = self.patronEsPalabra.findall(palabra)
        palabra = r[0] if r else ''
        return palabra

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
            rect = QRect(self.posicion_margen + offset.x(), -1,
                ancho + 1, self.viewport().height() + 3)
            fondo = QColor(recursos.COLOR_EDITOR['fondo-margen'])
            fondo.setAlpha(recursos.COLOR_EDITOR['opacidad'])
            pintar.fillRect(rect, fondo)
            pintar.drawRect(rect)
            pintar.drawLine(self.posicion_margen + offset.x(), 0,
                self.posicion_margen + offset.x(), self.viewport().height())
            pintar.end()

    def resaltar_linea_actual(self):
        """ Pinta la linea actual en donde está posicionado el cursor. """

        self.emit(SIGNAL("cursorPositionChange(int, int)"),
            self.textCursor().blockNumber() + 1,
            self.textCursor().columnNumber())

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

        if configuraciones.CHECK_INDENTACION:
            self.textCursor().insertText(' ' * configuraciones.INDENTACION)
            return True
        return False

    def _auto_indentar(self, evento):
        """ Inserta automáticamente 4 espacios después de presionar Enter,
        previamente escrito '{' """
        if configuraciones.CHECK_AUTO_INDENTACION:
            texto = self.textCursor().block().previous().text()
            espacios = self.__indentacion(texto, configuraciones.INDENTACION)
            self.textCursor().insertText(espacios)

            cursor = self.textCursor()
            cursor.setPosition(cursor.position())
            self.setTextCursor(cursor)

    def _completar_braces(self, evento):
        dic_braces = {'(': ')', '{': '}', '[': ']'}

        brace = str(evento.text())
        brac = dic_braces.get(brace)
        self.textCursor().insertText(brac)
        self.moveCursor(QTextCursor.Left)

    def devolver_texto(self):
        """ Retorna todo el contenido del editor """
        #print self.ID
        return unicode(self.toPlainText())

    def __tecla_backspace(self, event):
        if self.textCursor().hasSelection():
            return False

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        texto = str(cursor.selection().toPlainText())

        if(len(texto) % configuraciones.INDENTACION == 0) and texto.isspace():
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                configuraciones.INDENTACION)
            cursor.removeSelectedText()

            return True

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

    def convertir_a_mayusculas(self):
        self.textCursor().beginEditBlock()
        if self.textCursor().hasSelection():
            texto = str(self.textCursor().selectedText()).upper()
        else:
            texto = str(self.texto_abajo()).upper()
            self.moveCursor(QTextCursor.StartOfWord)
            self.moveCursor(QTextCursor.EndOfWord,
                QTextCursor.KeepAnchor)
        self.textCursor().insertText(texto)
        self.textCursor().endEditBlock()

    def convertir_a_minusculas(self):
        self.textCursor().beginEditBlock()
        if self.textCursor().hasSelection():
            texto = str(self.textCursor().selectedText()).lower()
        else:
            texto = str(self.texto_abajo()).lower()
            self.moveCursor(QTextCursor.StartOfWord)
            self.moveCursor(QTextCursor.EndOfWord,
                QTextCursor.KeepAnchor)
            self.textCursor().insertText(texto)
            self.textCursor().endEditBlock()

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

    def saltar_a_linea(self, linea=None):
        if linea is not None:
            self.emit(SIGNAL("addBackItemNavigation()"))
            self.ir_a_linea(linea)
            return

    def ir_a_linea(self, linea):
        self.unfold_blocks_for_jump(linea)
        if self.blockCount() >= linea:
            cursor = self.textCursor()
            cursor.setPosition(self.document().findBlockByLineNumber(
                linea).position())
            self.setTextCursor(cursor)

    def unfold_blocks_for_jump(self, linea):
        for l in self.widget_num_lineas._foldedBlocks:
            if linea >= l:
                self.widget_num_lineas.code_folding_event(l + 1)
            else:
                break

    def indentar_mas(self):
        cursor = self.textCursor()
        bloque = self.document().findBlock(cursor.selectionStart())
        fin = self.document().findBlock(cursor.selectionEnd()).next()

        cursor.beginEditBlock()

        cursor.setPosition(bloque.position())

        while bloque != fin:
            cursor.setPosition(bloque.position())
            cursor.insertText(' ' * configuraciones.INDENTACION)
            bloque = bloque.next()

        cursor.endEditBlock()

    def indentar_menos(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.EndOfLine)

        bloque = self.document().findBlock(cursor.selectionStart())
        fin = self.document().findBlock(cursor.selectionEnd()).next()

        cursor.beginEditBlock()

        cursor.setPosition(bloque.position())

        while bloque != fin:
            cursor.setPosition(bloque.position())
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                configuraciones.INDENTACION)
            texto = cursor.selectedText()
            if texto == ' ' * configuraciones.INDENTACION:
                cursor.removeSelectedText()
            bloque = bloque.next()

        cursor.endEditBlock()

    def _guardado(self, uA=False):
        if not uA:
            self.emit(SIGNAL("fileSaved(QPlainTextEdit)"), self)
            self.nuevo_archivo = False
            self.texto_modificado = False
            self.document().setModified(self.texto_modificado)

    def __indentacion(self, linea, ind=configuraciones.INDENTACION):
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