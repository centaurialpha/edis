# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QColor,
    QToolTip,
    QFont,
    QFontMetrics
    )

from PyQt4.QtCore import (
    pyqtSignal,
    Qt,
    QThread,
    SIGNAL
    )
from PyQt4.Qsci import QsciScintilla, QsciAPIs

from src import editor_scheme
from src.ui.editor import (
    checker,
    lexer,
    base,
    minimap,
    keywords
    )
from src.helpers import settings

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

    # Marcadores
    _marker_modified = 8
    _marker_save = 9

    # Señales
    _modificado = pyqtSignal(bool, name='archivo_modificado')
    fileSaved = pyqtSignal('PyQt_PyObject')
    _undo = pyqtSignal(['PyQt_PyObject'], name='accion_undo')
    _drop = pyqtSignal(['PyQt_PyObject'], name='dropSignal')
    linesChanged = pyqtSignal(int)

    def __init__(self):
        super(Editor, self).__init__()
        #FIXME: display
        self.__display = ""
        self._filename = ""
        self.modified = False
        self.is_new = True
        self._font = None
        # Configuration
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(settings.get_setting('editor/indent'))
        self.setBackspaceUnindents(True)
        # Quita el scrollbar
        self.send("sci_sethscrollbar", 0)
        # Configuración de indicadores
        self._word_indicator = 0
        self._warning_indicator = 1
        self._error_indicator = 2
        self.send("sci_indicsetstyle", self._word_indicator, "indic_box")
        self.send("sci_indicsetfore", self._word_indicator,
            QColor("#ccd900"))
        self.send("sci_indicsetstyle", self._warning_indicator, "indic_dots")
        self.send("sci_indicsetfore", self._warning_indicator,
            QColor("#ffff00"))
        self.send("sci_indicsetstyle", self._error_indicator, "indic_dots")
        # Scheme
        self.scheme = editor_scheme.get_scheme(
            settings.get_setting('editor/scheme'))
        # Folding
        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setFoldMarginColors(QColor(self.scheme['FoldMarginBack']),
                                 QColor(self.scheme['FoldMarginFore']))
        self.markerDefine(QsciScintilla.SC_MARK_LEFTRECT, self._marker_modified)
        self.setMarkerBackgroundColor(QColor(255, 0, 0), self._marker_modified)
        self.markerDefine(QsciScintilla.SC_MARK_LEFTRECT, self._marker_save)
        self.setMarkerBackgroundColor(QColor(0, 210, 0), self._marker_save)

        # Actualiza flags (espacios en blanco, cursor, sidebar, etc)
        self.update_options()
        # Lexer
        self._lexer = lexer.Lexer()
        self.setLexer(self._lexer)
        # Autocompletado
        self.api = None
        if settings.get_setting('editor/completion'):
            self.active_code_completion()
        # Indentación
        self.indentation = settings.get_setting('editor/width-indent')
        self.send("sci_settabwidth", self.indentation)
        # Minimapa
        self.minimap = None
        if settings.get_setting('editor/show-minimap'):
            self.minimap = minimap.Minimap(self)
            self.connect(self, SIGNAL("textChanged()"),
                         self.minimap.update_code)
        # Thread ocurrencias
        self.hilo_ocurrencias = ThreadBusqueda()
        self.connect(self.hilo_ocurrencias,
                     SIGNAL("ocurrenciasThread(PyQt_PyObject)"),
                     self.mark_words)
        # Analizador de estilo de código
        self.checker = None
        if settings.get_setting('editor/style-checker'):
            self.load_checker()
        # Fuente
        font = settings.get_setting('editor/font')
        font_size = settings.get_setting('editor/size-font')
        self.load_font(font, font_size)
        self.setMarginsBackgroundColor(QColor(self.scheme['SidebarBack']))
        self.setMarginsForegroundColor(QColor(self.scheme['SidebarFore']))
        # Línea actual
        self.send("sci_setcaretlinevisible",
                  settings.get_setting('editor/show-caret-line'))
        self.send("sci_setcaretlineback", QColor(self.scheme['CaretLineBack']))
        self.send("sci_setcaretfore", QColor(self.scheme['CaretLineFore']))
        self.send("sci_setcaretlinebackalpha", self.scheme['CaretLineAlpha'])
        # Cursor
        caret_period = settings.get_setting('editor/cursor-period')
        self.send("sci_setcaretperiod", caret_period)
        # Márgen
        if settings.get_setting('editor/show-margin'):
            self.update_margin()
        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor(
            self.scheme['MatchedBraceBack']))
        self.setMatchedBraceForegroundColor(QColor(
            self.scheme['MatchedBraceFore']))
        self.setUnmatchedBraceBackgroundColor(QColor(
            self.scheme['UnmatchedBraceBack']))
        self.setUnmatchedBraceForegroundColor(QColor(
            self.scheme['UnmatchedBraceFore']))

        # Conexiones
        self.connect(self, SIGNAL("linesChanged()"), self.update_sidebar)
        self.connect(self, SIGNAL("textChanged()"), self._add_marker_modified)

    def load_font(self, fuente, tam):
        self._font = QFont(fuente, tam)
        if self._lexer is None:
            self.setFont(self._font)
        else:
            self._lexer.setFont(self._font)
        self.setMarginsFont(self._font)

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

    #FIXME: Mejorar esto, solo es usado por el selector
    def get_display(self):
        return self.__display

    def set_display(self, name):
        self.__display = name

    display = property(get_display, set_display)

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

    def update_options(self):
        """ Actualiza las opciones del editor """

        if settings.get_setting('editor/show-tabs-spaces'):
            self.setWhitespaceVisibility(self.WsVisible)
        else:
            self.setWhitespaceVisibility(self.WsInvisible)
        self.setIndentationGuides(settings.get_setting('editor/show-guides'))
        if settings.get_setting('editor/wrap-mode'):
            self.setWrapMode(self.WrapWord)
        else:
            self.setWrapMode(self.WrapNone)
        self.send("sci_setcaretstyle", settings.get_setting('editor/cursor'))
        self.setCaretWidth(settings.get_setting('editor/caret-width'))
        self.setAutoIndent(settings.get_setting('editor/indent'))
        self.send("sci_setcaretperiod",
                  settings.get_setting('editor/cursor-period'))

    def update_sidebar(self):
        """ Ajusta el ancho del sidebar """
        fmetrics = QFontMetrics(self._font)
        lines = str(self.lines()) + '00'
        if len(lines) != 1:
            width = fmetrics.width(lines)
            self.setMarginWidth(0, width)

    def update_margin(self):
        """ Actualiza el ancho del márgen de línea """

        if settings.get_setting('editor/show-margin'):
            self.setEdgeMode(QsciScintilla.EdgeLine)
            ancho = settings.get_setting('editor/width-margin')
            self.setEdgeColumn(ancho)
            self.setEdgeColor(QColor(self.scheme['Margin']))
        else:
            self.setEdgeMode(QsciScintilla.EdgeNone)

    def update_indentation(self):
        ancho = settings.get_setting('editor/width-indent')
        self.send("sci_settabwidth", ancho)
        self.indentation = ancho

    def mark_words(self, palabras):
        self.clear_indicators(self._word_indicator)
        for p in palabras:
            self.fillIndicatorRange(p[0], p[1], p[0], p[2],
                                    self._word_indicator)

    def active_code_completion(self, enabled=True):
        if self.api is not None and enabled:
            return
        if enabled:
            self.api = QsciAPIs(self._lexer)
            # Agrego keywords a la API
            for keyword in keywords.keywords:
                self.api.add(keyword)
            self.api.prepare()
            self.setAutoCompletionThreshold(3)
            self.setAutoCompletionSource(QsciScintilla.AcsAll)
        else:
            self.api = None
            self.setAutoCompletionSource(0)

    def _add_marker_modified(self):
        """ Agrega el marcador cuando el texto cambia """

        nline, _ = self.getCursorPosition()
        if self.markersAtLine(nline):
            self.markerDelete(nline)
        self.markerAdd(nline, self._marker_modified)

    def _show_violations(self):
        data = self.checker.data
        self.clear_indicators(self._warning_indicator)
        for line, message in list(data.items()):
            line = int(line) - 1
            self.fillIndicatorRange(line, 0, line, self.lineLength(line),
                                    self._warning_indicator)

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
            self.hilo_ocurrencias.buscar(word, self.text())

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
            self.minimap.update_geometry()

    def comment(self):
        #FIXME: tener en cuenta /* */
        #FIXME: no funciona si el comentario no inicia en el índice 0
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

    def saved(self):
        self.fileSaved.emit(self)
        self.is_new = False
        self.modified = False
        self.setModified(False)
        # Itera todas las líneas y si existe un _marker_modified agrega
        # un _marker_save
        for nline in range(self.lines()):
            if self.markersAtLine(nline):
                self.markerAdd(nline, self._marker_save)

    def dropEvent(self, evento):
        self._drop.emit(evento)