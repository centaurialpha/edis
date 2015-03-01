# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QColor,
    QToolTip,
    QFont
    )

from PyQt4.QtCore import (
    pyqtSignal,
    Qt,
    QThread,
    SIGNAL
    )
from PyQt4.Qsci import QsciScintilla

from src import recursos
from src.ui.editor import (
    checker,
    lexer,
    base,
    minimap
    )
from src.helpers.configurations import ESettings

#FIXME: Cambiar comentario '//' (C++ style) por '/* */' (C style)


class ThreadBusqueda(QThread):
    """ Éste hilo busca ocurrencias de una palabra en el código fuente """

    def run(self):
        found_list = []
        found_generator = self.ffind_with_lines(self._text, self._word)
        for i in found_generator:
            found_list.append([i[2], i[0], i[1]])

        self.emit(SIGNAL("ocurrenciasThread(PyQt_PyObject)"), found_list)

    def ffind_with_lines(self, text, word):
        for line_number, line in enumerate(text.splitlines()):
            for index, end in self.ffind(line, word):
                yield index, end, line_number

    def ffind(self, text, word):
        i = 0
        while True:
            i = text.find(word, i)
            if i == -1:
                return
            end = i + len(word)
            yield i, end
            i += len(word)

    def buscar(self, word, source):
        self._text = source
        self._word = word

        # Run!
        self.start()


class Editor(base.Base):

    # Estilo
    _tema = recursos.TEMA

    # Señales
    _modificado = pyqtSignal(bool, name='archivo_modificado')
    fileSaved = pyqtSignal('PyQt_PyObject')
    _undo = pyqtSignal(['PyQt_PyObject'], name='accion_undo')
    _drop = pyqtSignal(['PyQt_PyObject'], name='dropSignal')
    linesChanged = pyqtSignal(int)

    def __init__(self):
        super(Editor, self).__init__()
        self._filename = ""
        self.texto_modificado = False
        self.is_new = True
        self.guardado_actualmente = False
        # Actualiza flags (espacios en blanco, cursor, sidebar, etc)
        self.actualizar()
        # Lexer
        self._lexer = lexer.Lexer()
        self.setLexer(self._lexer)
        # Autocompletado
        #FIXME: autocompletado
        #api = QsciAPIs(self._lexer)
        #for palabra in keywords.keywords:
            #api.add(palabra)
        #api.prepare()
        #self.setAutoCompletionThreshold(1)
        #self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        # Indentación
        self._indentacion = ESettings.get('editor/width-indent')
        self.send("sci_settabwidth", self._indentacion)
        # Minimapa
        self.minimap = None
        if ESettings.get('editor/show-minimap'):
            self.minimap = minimap.MiniMapa(self)
            self.connect(self, SIGNAL("selectionChanged()"),
                         self.minimap.area)
            self.connect(self, SIGNAL("textChanged()"),
                         self.minimap.actualizar_codigo)
        # Thread ocurrencias
        self.hilo_ocurrencias = ThreadBusqueda()
        self.connect(self.hilo_ocurrencias,
                     SIGNAL("ocurrenciasThread(PyQt_PyObject)"),
                     self.marcar_palabras)
        # Analizador de estilo de código
        self.checker = None
        if ESettings.get('editor/style-checker'):
            self.load_checker()
        # Fuente
        fuente = ESettings.get('editor/font')
        tam_fuente = ESettings.get('editor/size-font')
        self.cargar_fuente(fuente, tam_fuente)
        self.setMarginsBackgroundColor(QColor(self._tema['sidebar-fondo']))
        self.setMarginsForegroundColor(QColor(self._tema['sidebar-fore']))

        # Línea actual, cursor
        self.caret_line(self._tema['caret-background'],
                        self._tema['caret-line'], self._tema['caret-opacidad'])
        # Márgen
        if ESettings.get('editor/show-margin'):
            self.actualizar_margen()

        # Brace matching
        self.match_braces(QsciScintilla.SloppyBraceMatch)
        self.match_braces_color(self._tema['brace-background'],
                                self._tema['brace-foreground'])
        self.unmatch_braces_color(self._tema['brace-unbackground'],
                                  self._tema['brace-unforeground'])

    def cargar_fuente(self, fuente, tam):
        self._fuente = QFont(fuente, tam)
        if self._lexer is None:
            self.setFont(self._fuente)
        else:
            self._lexer.setFont(self._fuente)
        self.setMarginsFont(self._fuente)

    def load_checker(self, activated=True):
        if activated and self.checker is not None:
            return
        if not activated:
            self.checker = None
            self.clear_indicators(self._warning_indicator)
        else:
            self.checker = checker.Checker(self)
            self.connect(self.checker, SIGNAL("finished()"),
                         self._show_violations)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):  # lint:ok
        self._filename = new_filename
        if new_filename:
            self.is_new = False
        if self.checker is not None:
            self.checker.start_checker()

    def actualizar(self):
        """ Actualiza las opciones del editor """

        if ESettings.get('editor/show-tabs-spaces'):
            self.setWhitespaceVisibility(self.WsVisible)
        else:
            self.setWhitespaceVisibility(self.WsInvisible)
        self.setIndentationGuides(ESettings.get('editor/show-guides'))
        if ESettings.get('editor/wrap-mode'):
            self.setWrapMode(self.WrapWord)
        else:
            self.setWrapMode(self.WrapNone)
        self.send("sci_setcaretstyle", ESettings.get('editor/cursor'))

    @property
    def altura_lineas(self):
        linea, i = self.devolver_posicion_del_cursor()
        return self.textHeight(linea)

    def devolver_posicion_del_cursor(self):
        """ Posición del cursor (línea, columna) """

        return self.getCursorPosition()

    def actualizar_margen(self):
        """ Actualiza el ancho del márgen de línea """

        if ESettings.get('editor/show-margin'):
            self.setEdgeMode(QsciScintilla.EdgeLine)
            ancho = ESettings.get('editor/width-margin')
            self.setEdgeColumn(ancho)
            self.setEdgeColor(QColor(self._tema['margen']))
        else:
            self.setEdgeMode(QsciScintilla.EdgeNone)

    def actualizar_indentacion(self):
        ancho = ESettings.get('editor/width-indent')
        self.send("sci_settabwidth", ancho)
        self._indentacion = ancho

    def marcar_palabras(self, palabras):
        self.clear_indicators(self._word_indicator)
        for p in palabras:
            self.fillIndicatorRange(p[0], p[1], p[0], p[2],
                                    self._word_indicator)

    def _show_violations(self):
        data = self.checker.data
        self.clear_indicators(self._warning_indicator)
        for line, message in list(data.items()):
            line = int(line) - 1
            self.fillIndicatorRange(line, 0, line, self.lineLength(line),
                                    self._warning_indicator)

    def buscar(self, palabra, re=False, cs=False, wo=False, wrap=False,
               forward=True, linea=-1, indice=-1):
        """ Buscar la primera aparición de @palabra,
        si se encuentra se selecciona.

        @palabra: palabra buscada.
        @re: expresión regular en lugar de una cadena simple.
        @cs: case sensitive
        @wo: busca toda la palabra, si es falso cualquier texto coincidente
        @wrap: envoltura
        """

        pass

    def replace_word(self, reemplazar, reemplazo, todo=False):
        """ Reemplaza una o varias ocurrencias de @reemplazar por @reemplazo """

        pass

    def _text_under_cursor(self):
        """ Texto seleccionado con el cursor """

        line, index = self.getCursorPosition()  # Posición del cursor
        word = self.wordAtLineIndex(line, index)  # Palabra en esa pos
        return word

    def mouseReleaseEvent(self, e):
        super(Editor, self).mouseReleaseEvent(e)
        if e.button() == Qt.LeftButton:
            word = self._text_under_cursor()
            if not word:
                self.clear_indicators(self._word_indicator)
                return
            self.hilo_ocurrencias.buscar(word, self.texto)

    def mouseMoveEvent(self, event):
        super(Editor, self).mouseMoveEvent(event)
        if self.checker is None:
            return
        position = event.pos()
        line = str(self.lineAt(position) + 1)
        message = self.checker.data.get(line, None)
        if message is not None:
            QToolTip.showText(self.mapToGlobal(position), message)

    def keyReleaseEvent(self, event):
        super(Editor, self).keyReleaseEvent(event)
        line, _ = self.getCursorPosition()
        self.linesChanged.emit(line)

    def keyPressEvent(self, e):
        super(Editor, self).keyPressEvent(e)
        if e.key() == Qt.Key_Escape:
            self.clear_indicators(self._word_indicator)

    def resizeEvent(self, e):
        super(Editor, self).resizeEvent(e)
        if self.minimap is not None:
            self.minimap.redimensionar()

    def comment(self):
        if self.hasSelectedText():
            line_from, _, line_to, _ = self.getSelection()

            # Iterar todas las líneas seleccionadas
            self.send("sci_beginundoaction")
            for line in range(line_from, line_to + 1):
                self.insertAt('//', line, 0)
            self.send("sci_endundoaction")
        else:
            line = self.devolver_posicion_del_cursor()[0]
            self.insertAt('//', line, 0)

    def uncomment(self):
        if self.hasSelectedText():
            line_from, _, line_to, _ = self.getSelection()
            self.send("sci_beginundoaction")
            for line in range(line_from, line_to + 1):
                self.setSelection(line, 0, line, 2)
                if not self.text(line).startswith('//'):
                    continue
                self.removeSelectedText()
            self.send("sci_endundoaction")
        else:
            line, _ = self.getCursorPosition()
            if not self.text(line).startswith('//'):
                return
            self.setSelection(line, 0, line, 2)
            self.removeSelectedText()

    def to_lowercase(self):
        if self.hasSelectedText():
            text = self.selectedText().lower()
        else:
            line, _ = self.getCursorPosition()
            text = self.text(line).lower()
            self.setSelection(line, 0, line, len(text))
        self.replaceSelectedText(text)

    def to_uppercase(self):
        if self.hasSelectedText():
            text = self.selectedText().upper()
        else:
            line, _ = self.getCursorPosition()
            text = self.text(line).upper()
            self.setSelection(line, 0, line, len(text))
        self.replaceSelectedText(text)

    def to_title(self):
        if self.hasSelectedText():
            text = self.selectedText().title()
        else:
            line, _ = self.getCursorPosition()
            text = self.text(line).title()
            self.setSelection(line, 0, line, len(text))
        self.replaceSelectedText(text)

    def duplicate_line(self):
        self.send("sci_lineduplicate")

    def delete_line(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, desde_indice, hasta, _ = self.getSelection()
            self.setCursorPosition(desde, desde_indice)
            while desde != hasta:
                self.send("sci_linedelete")
                desde += 1
            self.send("sci_endundoaction")
        else:
            self.send("sci_linedelete")

    def indent_more(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, _, hasta, _ = self.getSelection()
            for linea in range(desde, hasta + 1):
                self.indent(linea)
            self.send("sci_endundoaction")
        else:
            linea, _ = self.devolver_posicion_del_cursor()
            self.indent(linea)

    def indent_less(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, _, hasta, _ = self.getSelection()
            for linea in range(desde, hasta + 1):
                self.unindent(linea)
            self.send("sci_endundoaction")
        else:
            linea, _ = self.devolver_posicion_del_cursor()
            self.unindent(linea)

    def move_down(self):
        self.send("sci_moveselectedlinesdown")

    def move_up(self):
        self.send("sci_moveselectedlinesup")

    def guardado(self):
        self.fileSaved.emit(self)
        self.is_new = False
        self.texto_modificado = False
        self.setModified(False)

    def dropEvent(self, evento):
        self._drop.emit(evento)