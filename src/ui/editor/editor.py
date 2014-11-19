#-*- coding: utf-8 -*-

# <Editor.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

# Módulos Python
import re
from tokenize import generate_tokens, TokenError
import token as tkn
#lint:disable
try:
    from StringIO import StringIO
except:
    # Python 3
    from io import StringIO
#lint:enable

# Módulos QtGui
from PyQt4.QtGui import (
    QPlainTextEdit,
    QBrush,
    QTextEdit,
    QColor,
    QFontMetricsF,
    QPainter,
    QFont,
    QTextCursor,
    QTextOption,
    QTextDocument,
    QTextCharFormat,
    )

# Módulos Qtcore
from PyQt4.QtCore import (
    Qt,
    SIGNAL,
    QString
    )

from PyQt4.Qt import (
    QVariant,
    QTextFormat
    )

# Módulos EDIS
from src import recursos
from src.helpers import configuraciones
from src.ui import tabitem
from src.ui.editor import (
    minimapa,
    acciones_,
    widget_numero_lineas,
    )
from src.ui.editor.highlighter_ import Highlighter

# Diccionario teclas
TECLA = {
    'TABULACION': Qt.Key_Tab,
    'ENTER': Qt.Key_Return,
    'LLAVE': Qt.Key_BraceLeft,
    'LLAVE-D': Qt.Key_BraceRight,
    'PARENTESIS': Qt.Key_ParenLeft,
    'PARENTESIS-D': Qt.Key_ParenRight,
    'CORCHETE': Qt.Key_BracketLeft,
    'CORCHETE-D': Qt.Key_BracketRight,
    'BACKSPACE': Qt.Key_Backspace,
    'COMILLAS': Qt.Key_Apostrophe,
    'COMILLAS-D': Qt.Key_QuoteDbl
    }

BRACES = configuraciones.BRACES
COMILLAS = configuraciones.COMILLAS


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
        self.guia_indentacion = 0
        self.nuevo_archivo = True
        self.patronEsPalabra = re.compile('\w+')
        self.guardado_actualmente = False
        self.widget_num_lineas = None
        self.highlighter = None
        self.minimapa = None
        self.palabra_seleccionada = ''
        self.braces = None
        self.extraSelections = []
        # Carga el tema de editor
        self.estilo_editor()
        # Completador
        #FIXME: completador
        self.completador = None
        # Carga el tipo de letra
        self._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        # Sidebar
        if configuraciones.SIDEBAR:
            self.widget_num_lineas = widget_numero_lineas.NumeroDeLineaBar(self)

        # Resaltado en posición del cursor
        self.resaltar_linea_actual()

        self.prePresionado = {
            TECLA.get('TABULACION'): self._indentar,
            TECLA.get('BACKSPACE'): self.__tecla_backspace,
            #TECLA.get('LLAVE-D'): self.autocompletar_braces,
            TECLA.get('CORCHETE-D'): self.autocompletar_braces,
            TECLA.get('PARENTESIS-D'): self.autocompletar_braces,
            TECLA.get('COMILLAS'): self.autocompletar_comillas,
            TECLA.get('COMILLAS-D'): self.autocompletar_comillas
            }

        self.postPresionado = {
            TECLA.get('ENTER'): self._auto_indentar,
            #TECLA.get('LLAVE'): self.autocompletado_braces,
            TECLA.get('CORCHETE'): self.autocompletado_braces,
            TECLA.get('PARENTESIS'): self.autocompletado_braces,
            TECLA.get('COMILLAS'): self.autocompletado_comillas,
            TECLA.get('COMILLAS-D'): self.autocompletado_comillas
            }

        self.connect(self, SIGNAL("undoAvailable(bool)"), self._guardado)
        self.connect(self, SIGNAL("cursorPositionChanged()"),
            self.resaltar_linea_actual)
        #self.connect(self, SIGNAL("blockCountChanged(int)"),
            #self.actualizar_metadata)
        if self.widget_num_lineas is not None:
            self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                self.widget_num_lineas.actualizar_area)

        # Minimapa
        if configuraciones.MINIMAPA:
            self.minimapa = minimapa.MiniMapa(self)
            self.minimapa.show()
            self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                self.minimapa.actualizar_area_visible)
            self.minimapa.highlighter = Highlighter(self.minimapa.document(),
                recursos.NUEVO_TEMA)

    def print_linea(self, l):
        print(l)

    def set_id(self, id_):
        super(Editor, self).set_id(id_)
        if self.minimapa:
            self.minimapa.set_code(self.toPlainText())

    def estilo_editor(self):
        """ Aplica estilos de colores al editor """
        if self.highlighter is None:
            self.highlighter = Highlighter(self.document(), recursos.NUEVO_TEMA)

        tema_editor = 'QPlainTextEdit {color: %s; background-color: %s;' \
        'selection-background-color: %s; selection-color: %s;}' \
        % (recursos.NUEVO_TEMA.get('texto-editor',
        recursos.TEMA_EDITOR['texto-editor']),
        recursos.NUEVO_TEMA.get('fondo-editor',
        recursos.TEMA_EDITOR['fondo-editor']),
        recursos.NUEVO_TEMA.get('fondo-seleccion-editor',
        recursos.TEMA_EDITOR['fondo-seleccion-editor']),
        recursos.NUEVO_TEMA.get('seleccion-editor',
        recursos.TEMA_EDITOR['seleccion-editor']))
        self.setStyleSheet(tema_editor)

    def set_flags(self):
        if not configuraciones.MODO_ENVOLVER:
            self.setWordWrapMode(QTextOption.NoWrap)
        else:
            self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
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

    def resizeEvent(self, event):
        """ Redimensiona la altura del widget. """

        QPlainTextEdit.resizeEvent(self, event)
        if self.widget_num_lineas is not None:
            self.widget_num_lineas.setFixedHeight(self.height())
        if self.minimapa:
            self.minimapa.ajustar_()

    def wheelEvent(self, evento):
        if evento.modifiers() == Qt.ControlModifier:
            if evento.delta() == 120:
                self.acercar()
            elif evento.delta() == -120:
                self.alejar()
            evento.ignore()
        QPlainTextEdit.wheelEvent(self, evento)

    def devolver_cantidad_de_lineas(self):
        return self.blockCount()

    def texto_abajo(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        palabra = cursor.selectedText()
        r = self.patronEsPalabra.findall(palabra)
        palabra = r[0] if r else ''
        return palabra

    def buscar_match(self, palabra, banderas, buscarSgt=False):
        banderas = QTextDocument.FindFlags(banderas)
        if buscarSgt:
            self.moveCursor(QTextCursor.NoMove, QTextCursor.KeepAnchor)
        else:
            self.moveCursor(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        f = self.find(palabra, banderas)
        if not f:
            cursor = self.textCursor()
            self.moveCursor(QTextCursor.Start)
            f = self.find(palabra, banderas)
            if not f:
                self.setTextCursor(cursor)

    def set_selection_from_pair(self, inicio, fin):
        cursor = self.textCursor()
        cursor.setPosition(inicio)
        cursor.setPosition(fin, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def paintEvent(self, event):
        """ Evento que dibuja el margen de línea."""

        QPlainTextEdit.paintEvent(self, event)
        if configuraciones.MOSTRAR_MARGEN:
            pintar = QPainter()
            pintar.begin(self.viewport())
            pintar.setPen(QColor(recursos.NUEVO_TEMA.get('margen-linea',
                recursos.TEMA_EDITOR['margen-linea'])))
            offset = self.contentOffset()
            #ancho = self.viewport().width() - (self.posicion_margen +
                #offset.x())
            #rect = QRect(self.posicion_margen + offset.x(), -1,
                #ancho + 1, self.viewport().height() + 5)
            fondo = QColor(recursos.NUEVO_TEMA.get('fondo-margen',
                recursos.TEMA_EDITOR['fondo-margen']))
            fondo.setAlpha(configuraciones.OPACIDAD_MARGEN)
            #pintar.fillRect(rect, fondo)
            #pintar.drawRect(rect)
            pintar.drawLine(self.posicion_margen + offset.x(), 0,
                self.posicion_margen + offset.x(), self.viewport().height())
            pintar.end()

        if configuraciones.GUIA_INDENTACION:
            altura = self.viewport().height()
            offset = self.contentOffset()
            pintar = QPainter()
            pintar.begin(self.viewport())
            color = QColor('gray')
            brush = QBrush(color, 10)
            pintar.setBackground(brush)
            color.setAlpha(100)
            pintar.setPen(color)
            pintar.pen().setCosmetic(True)
            altura_char = self.fontMetrics().height()
            bloque = self.firstVisibleBlock()
            previous_line = []

            while bloque.isValid():
                geo = self.blockBoundingGeometry(bloque)
                geo.translate(offset)
                posicion_y = geo.top()
                if posicion_y > altura:
                    break
                col = (len(acciones_.devolver_espacios(
                    bloque.text())) // configuraciones.INDENTACION)
                if col == 0:
                    for l in previous_line:
                        pintar.drawLine(
                            l, posicion_y, l, posicion_y + altura_char)
                else:
                    previous_line = []
                for i in range(1, col):
                    posicion_linea = self.inicio_indentacion + (
                        self.guia_indentacion * (i - 1))
                    pintar.drawLine(posicion_linea, posicion_y, posicion_linea,
                        posicion_y + altura_char)
                    previous_line.append(posicion_linea)
                bloque = bloque.next()
            pintar.end()

    def resaltar_linea_actual(self):
        """ Pinta la linea actual en donde está posicionado el cursor. """

        self.emit(SIGNAL("cursorPositionChange(int, int)"),
            self.textCursor().blockNumber() + 1,
            self.textCursor().columnNumber())
        self.extraSelections = []

        seleccion = QTextEdit.ExtraSelection()
        #color = QColor(recursos.NUEVO_TEMA.get('linea-actual',
            #recursos.TEMA_EDITOR['linea-actual']))
        color = QColor('lightblue').lighter(120)
        #color.setAlpha(40)
        seleccion.format.setBackground(color)
        seleccion.format.setProperty(
            QTextFormat.FullWidthSelection, QVariant(True))
        seleccion.cursor = self.textCursor()
        seleccion.cursor.clearSelection()
        self.extraSelections.append(seleccion)

        extra = self.resaltar_braces()
        if extra:
            self.extraSelections.extend(extra)
        self.setExtraSelections(self.extraSelections)

    def resaltar_braces(self):
        # Basado en: https://gitorious.org/khteditor

        izquierdo, derecho = QTextEdit.ExtraSelection(),\
                      QTextEdit.ExtraSelection()

        cursor = self.textCursor()
        bloque = cursor.block()

        data = bloque.userData()
        anterior, siguiente = None, None

        if data is not None:
            posicion = cursor.position()
            pos_bloque = cursor.block().position()
            braces = data.braces
            N = len(braces)

            for k in range(0, N):
                if braces[k].position == posicion - pos_bloque or\
                   braces[k].position == posicion - pos_bloque - 1:
                    anterior = braces[k].position + pos_bloque
                    if braces[k].character in ['{', '(', '[']:
                        siguiente = self.match_izq(bloque,
                                               braces[k].character,
                                               k + 1, 0)
                    elif braces[k].character in ['}', ')', ']']:
                        siguiente = self.match_der(bloque,
                                                braces[k].character,
                                                k, 0)

        if (siguiente is not None and siguiente > 0) \
            and (anterior is not None and anterior > 0):

            formato = QTextCharFormat()

            cursor.setPosition(anterior)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            formato.setForeground(QColor('white'))
            formato.setBackground(QColor('blue'))
            izquierdo.format = formato
            izquierdo.cursor = cursor

            cursor.setPosition(siguiente)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            formato.setForeground(QColor('white'))
            formato.setBackground(QColor('red'))
            derecho.format = formato
            derecho.cursor = cursor

            return izquierdo, derecho

        elif anterior is not None:
            formato = QTextCharFormat()

            cursor.setPosition(anterior)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            formato.setForeground(QColor('white'))
            formato.setBackground(QColor('red'))
            izquierdo.format = formato
            izquierdo.cursor = cursor
            return (izquierdo,)
        elif siguiente is not None:
            formato = QTextCharFormat()

            cursor.setPosition(siguiente)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            formato.setForeground(QColor('white'))
            formato.setBackground(QColor('green'))
            izquierdo.format = formato
            izquierdo.cursor = cursor
            return (izquierdo,)

    def match_izq(self, bloque, caracter, inicio, found):
        dic = {'{': '}', '(': ')', '[': ']'}
        bj = 0

        while bloque.isValid() and (bj < 20):
            data = bloque.userData()
            if data is not None:
                braces = data.braces
                N = len(braces)

                for k in range(inicio, N):
                    if braces[k].character == caracter:
                        found += 1
                    if braces[k].character == dic[caracter]:
                        if not found:
                            return braces[k].position + bloque.position()
                        else:
                            found -= 1
                bloque = bloque.next()
                bj += 1
                inicio = 0

    def match_der(self, bloque, caracter, inicio, found):
        dic = {'}': '{', ')': '(', ']': '['}
        bj = 0
        while bloque.isValid() and (bj < 20):
            data = bloque.userData()

            if data is not None:
                braces = data.braces

                if inicio is None:
                    inicio = len(braces)
                for k in range(inicio - 1, -1, -1):
                    if braces[k].character == caracter:
                        found += 1
                    if braces[k].character == dic[caracter]:
                        if found == 0:
                            return braces[k].position + bloque.position()
                        else:
                            found -= 1
                bloque = bloque.previous()
                bj += 1
                inicio = None

    def devolver_seleccion(self, inicio, fin):
        cursor = self.textCursor()
        cursor.setPosition(inicio)
        cursor2 = self.textCursor()
        if fin == QTextCursor.End:
            cursor2.movePosition(fin)
            cursor.setPosition(cursor2.position(), QTextCursor.KeepAnchor)
        else:
            cursor.setPosition(fin, QTextCursor.KeepAnchor)
        return unicode(cursor.selection().toPlainText())

    def __posicion_absoluta_en_texto(self, texto, pos):
        linea, pos_relativa = pos
        div_linea = linea - 1
        longitud = 0
        for cada_linea in texto.splitlines()[:div_linea]:
            longitud += len(cada_linea)
        return longitud + div_linea + pos_relativa

    def tokenize_text(self, texto):
        sintaxis_invalida = False
        token_buffer = []
        try:
        #texto = str(texto)
            for tkn_type, tkn_rep, tkn_begin, tkn_end, _ in \
                        generate_tokens(StringIO(texto).readline):
                token_buffer.append((tkn_type, tkn_rep, tkn_begin, tkn_end))
        except (TokenError, SyntaxError):
            sintaxis_invalida = True
        return (sintaxis_invalida, token_buffer)

    def m_braces(self, pos, brace, adelante):
        # de NINJA-IDE
        brace_d = {')': '(', ']': '[', '(': ')', '[': ']'}
        braceM = brace_d[brace]
        if adelante:
            texto = self.devolver_seleccion(pos, QTextCursor.End)
        else:
            texto = self.devolver_seleccion(QTextCursor.Start, pos)

        braces = []
        brace_buffer = []
        sintaxis_invalida, tokens = self.tokenize_text(texto)
        for tkn_tipo, tkn_rep, tkn_inicio, tkn_fin in tokens:
            if(tkn_tipo == tkn.OP) and (tkn_rep in brace_d):
                tkn_pos = adelante and tkn_inicio or tkn_fin
                brace_buffer.append((tkn_rep, tkn_pos))
        if not adelante:
            brace_buffer.reverse()
        if adelante and (not sintaxis_invalida):
            brace_buffer = brace_buffer[1:]

        for tkn_rep, tkn_posicion in brace_buffer:
            if (tkn_rep == braceM) and not braces:
                hl_position = \
                self.__posicion_absoluta_en_texto(texto, tkn_posicion)
                return adelante and hl_position + pos or hl_position
            elif braces and \
                (brace_d.get(tkn_rep, '') == braces[-1]):
                braces.pop(-1)
            else:
                braces.append(tkn_rep)

    def keyPressEvent(self, evento):

        if self.prePresionado.get(evento.key(), lambda a: False)(evento):
            self.emit(SIGNAL("keyPressEvent(QEvent)"), evento)
            return
        self.texto_seleccionado = self.textCursor().selectedText()
        QPlainTextEdit.keyPressEvent(self, evento)

        self.postPresionado.get(evento.key(), lambda a: False)(evento)
        self.emit(SIGNAL("keyPressEvent(QEvent)"), evento)

    def _indentar(self, evento):
        """ Inserta 4 espacios si se presiona la tecla Tab """

        if configuraciones.CHECK_INDENTACION:
            self.textCursor().insertText(' ' * configuraciones.INDENTACION)
            return True
        return False

    def _auto_indentar(self, evento):
        """ Indentación automática y autocompletado de llave. """

        cursor = self.textCursor()
        if configuraciones.CHECK_AUTOINDENTACION:
            texto = cursor.block().previous().text()
            patron = re.compile('^\s+')
            indentacion = ''
            b = False
            tam = len(texto)
            if tam > 0 and texto[-1] == '{':
                b = True
                indentacion = ' ' * configuraciones.INDENTACION
            espacio = patron.match(texto)
            if espacio is not None:
                espacios = espacio.group() + indentacion
            else:
                espacios = indentacion
            cursor.insertText(espacios)
            if b:
                cursor.insertText('\n')
                if len(espacios) == configuraciones.INDENTACION:
                    #espacios = ''
                    cursor.insertText('')
                    cursor.insertText('}')
                    cursor.movePosition(QTextCursor.Left,
                                        QTextCursor.KeepAnchor, 2)
                else:
                    cursor.insertText(espacios)
                    #cursor.insertText('}')
                    cursor.movePosition(QTextCursor.Left,
                                        QTextCursor.KeepAnchor)
                    cursor.movePosition(QTextCursor.Left,
                                        QTextCursor.KeepAnchor,
                                        configuraciones.INDENTACION - 1)
                    cursor.removeSelectedText()
                    cursor.insertText('}')
                    cursor.movePosition(QTextCursor.StartOfLine,
                                        QTextCursor.KeepAnchor)
                    cursor.movePosition(QTextCursor.Left,
                                        QTextCursor.KeepAnchor)
            cursor.setPosition(cursor.position())
            self.setTextCursor(cursor)

    def autocompletado_braces(self, evento):
        dic_braces = {'(': ')', '[': ']'}
        brace = unicode(evento.text())
        if brace not in BRACES:
            return

        texto = self.textCursor().block().text()
        brace_complementario = QString(dic_braces.get(brace))
        buffer_ = []
        _, tokens = self.tokenize_text(texto)
        unb = 0
        for t_t, t_r, t_c, t_f in tokens:
            if t_r == brace:
                unb += 1
            elif t_r == brace_complementario:
                unb -= 1
            if t_r.strip():
                buffer_.append((t_r, t_f[1]))
            unb = (unb >= 0) and unb or 0
        if (len(buffer_) == 3) and (buffer_[2][0] == brace):
            self.textCursor().insertText(self.texto_seleccionado)
        elif buffer_ and (not unb) and self.texto_seleccionado:
            self.textCursor().insertText(self.texto_seleccionado)
        elif unb:
            self.textCursor().insertText(brace_complementario)
            self.moveCursor(QTextCursor.Left)
            self.textCursor().insertText(self.texto_seleccionado)

    def autocompletar_braces(self, evento):
        """ Mueve el cursor a la derecha si el autocompletado está activado,
        esto para no repetir el cerrado de un brace. """

        BRACE = {')': '(', ']': '[', '(': ')', '[': ']'}
        balance = False
        texto = unicode(evento.text())
        for texto in BRACES.values():
            porcion = self.reverse_texto_seleccionado(1, 1)
            brace_abierto = porcion[0]
            brace_cerrado = porcion[1] if len(porcion) > 1 else None
            if (BRACE.get(brace_abierto, None) == texto) and \
                (texto == brace_cerrado):
                balance = True
            if balance:
                self.moveCursor(QTextCursor.Right)
                return True

    def autocompletado_comillas(self, evento):
        #COMILLAS = {'"': '"', "'": "'"}
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        comilla = unicode(evento.text())
        if comilla in COMILLAS:
            self.textCursor().insertText(comilla)
            self.moveCursor(QTextCursor.Left)
            self.textCursor().insertText(self.texto_seleccionado)

    def autocompletar_comillas(self, evento):
        texto = unicode(evento.text())
        sup = False
        pre = self.reverse_texto_seleccionado(0, 3)
        pos = self.reverse_texto_seleccionado(3, 0)
        if pos[:1] == texto:
            pre = self.reverse_texto_seleccionado(0, 5)
            if pre == texto:
                sup = True
            elif pre[-1] == texto:
                sup = True
        if sup:
            self.moveCursor(QTextCursor.Right)
        return sup

    def reverse_texto_seleccionado(self, comienzo, fin):
        cursor = self.textCursor()
        pos_cursor = cursor.position()
        cursor.setPosition(pos_cursor + comienzo)
        while (cursor.position() == pos_cursor) and comienzo > 0:
            comienzo -= 1
            cursor.setPosition(pos_cursor + comienzo)
        cursor.setPosition(pos_cursor - fin, QTextCursor.KeepAnchor)
        texto_seleccionado = unicode(cursor.selectedText())
        return texto_seleccionado

    def devolver_texto(self):
        """ Retorna todo el contenido del editor """

        return unicode(self.toPlainText())

    def devolver_posicion_del_cursor(self):
        return self.textCursor().position()

    def __tecla_backspace(self, event):
        if self.textCursor().hasSelection():
            return False

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        texto = unicode(cursor.selection().toPlainText())
        if(len(texto) % configuraciones.INDENTACION == 0) and texto.isspace():
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                configuraciones.INDENTACION)
            cursor.removeSelectedText()

            return True

    def tabulaciones_por_espacios_en_blanco(self):
        acciones_.tabulaciones_por_espacios_en_blanco(self)

    def _cargar_fuente(self, fuente_=configuraciones.FUENTE,
        tam=configuraciones.TAM_FUENTE):

            fuente = QFont(fuente_, tam)
            self.document().setDefaultFont(fuente)
            self.actualizar_margen_linea(fuente)

    def acercar(self):
        """ Aumenta el tamaño de la fuente y actualiza el márgen. """

        fuente = self.document().defaultFont()
        tam = fuente.pointSize()

        if tam < configuraciones.FUENTE_MAX_TAM:
            tam += 1
            fuente.setPointSize(tam)

        self.setFont(fuente)
        self.actualizar_margen_linea(fuente)

    def alejar(self):
        """ Disminuye el tamaño de la fuente y actualiza el márgen. """

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

        self.char_width = f_metrics.averageCharWidth()
        if configuraciones.INDENTACION:
            self.guia_indentacion = self.char_width * \
                configuraciones.INDENTACION
            self.inicio_indentacion = (-(self.char_width / 2) +
                                self.guia_indentacion + self.char_width)

    def saltar_a_linea(self, linea=None):
        if linea is not None:
            self.emit(SIGNAL("addBackItemNavigation()"))
            self.ir_a_linea(linea)
            return

    def ir_a_linea(self, linea):
        self.desplegar_bloques_saltar(linea)
        if self.blockCount() >= linea:
            cursor = self.textCursor()
            cursor.setPosition(self.document().findBlockByLineNumber(
                linea).position())
            self.setTextCursor(cursor)

    def desplegar_bloques_saltar(self, linea):
        for l in self.widget_num_lineas.bloques_plegados:
            if linea >= l:
                self.widget_num_lineas.code_folding_event(l + 1)
            else:
                break

    def indentar_mas(self):
        """ Inserta indentación a un bloque de código. """

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
        """ Quita indentación a un bloque de código. """

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
            self.emit(SIGNAL("archivoGuardado(QPlainTextEdit)"), self)
            self.nuevo_archivo = False
            self.texto_modificado = False
            self.document().setModified(self.texto_modificado)


def crear_editor(nombre_archivo=''):
    editor = Editor(nombre_archivo)

    return editor