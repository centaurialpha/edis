# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

from PyQt4.QtGui import (
    QColor,
    QToolTip,
    QFont,
    QFontMetrics
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL
    )
from PyQt4.Qsci import QsciScintilla, QsciAPIs

from src import editor_scheme
from src.ui.editor import (
    checker,
    lexer,
    base,
    minimap,
    keywords,
    editor_helpers
    )
from src.core import settings

# FIXME: Cambiar comentario '//' (C++ style) por '/* */' (C style)

REGEX_STRUCT = re.compile("(typedef struct|struct)\s+\w+")


class Editor(base.Base):

    # Braces
    BRACE = {
        '(': ')',
        '[': ']'
        }

    # Quotes
    QUOTE = {
        "'": "'",
        '"': '"'
        }

    # Marcadores
    MARKER_MODIFIED = 3
    MARKER_SAVED = 4

    # Indicadores
    WORD_INDICATOR = 0
    WARNING_INDICATOR = 1

    def __init__(self, obj_file):
        super(Editor, self).__init__()
        self.obj_file = obj_file  # Asociación con el objeto EdisFile
        self._font = None
        # Configuration
        use_tabs = settings.get_setting('editor/usetabs')
        self.setIndentationsUseTabs(use_tabs)
        self.setAutoIndent(settings.get_setting('editor/indent'))
        self.setBackspaceUnindents(True)
        # Quita el scrollbar
        self.send("sci_sethscrollbar", 0)
        # Configuración de indicadores
        self.send("sci_indicsetstyle", Editor.WORD_INDICATOR, "indic_box")
        self.send("sci_indicsetfore", Editor.WORD_INDICATOR, QColor("#FF0000"))
        self.send("sci_indicsetstyle",
                  Editor.WARNING_INDICATOR, "indic_squiggle")
        self.send("sci_indicsetfore",
                  Editor.WARNING_INDICATOR, QColor("#0000FF"))
        # Scheme
        self.scheme = editor_scheme.get_scheme(
            settings.get_setting('editor/scheme'))
        # Folding
        self.setFolding(QsciScintilla.PlainFoldStyle)  # en márgen 2
        self.setMarginWidth(3, 5)  # 5px de espacios en márgen 3
        self.send("sci_markersetfore",
            QsciScintilla.SC_MARKNUM_FOLDER,
            QColor(self.scheme['FoldMarkerFore']))
        self.send("sci_markersetback",
            QsciScintilla.SC_MARKNUM_FOLDER,
            QColor(self.scheme['FoldMarkerBack']))
        self.setFoldMarginColors(QColor(self.scheme['FoldMarginBack']),
                                 QColor(self.scheme['FoldMarginFore']))
        self.markerDefine(QsciScintilla.SC_MARK_LEFTRECT,
                          Editor.MARKER_MODIFIED)
        self.setMarkerBackgroundColor(
            QColor(226, 192, 141), Editor.MARKER_MODIFIED)
        self.markerDefine(QsciScintilla.SC_MARK_LEFTRECT, Editor.MARKER_SAVED)
        self.setMarkerBackgroundColor(QColor(55, 142, 103),
                                      Editor.MARKER_SAVED)

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
        self._indentation = settings.get_setting('editor/width-indent')
        self.send("sci_settabwidth", self._indentation)
        # Minimapa
        self.minimap = None
        if settings.get_setting('editor/minimap'):
            self.minimap = minimap.Minimap(self)
            self.connect(self, SIGNAL("textChanged()"),
                         self.minimap.update_code)
        # Thread que busca palabras
        self.search_thread = editor_helpers.SearchThread()
        self.connect(self.search_thread,
                     SIGNAL("foundWords(PyQt_PyObject)"), self.mark_words)
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
        self.setBraceMatching(int(settings.get_setting('editor/match-brace')))
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

    @property
    def filename(self):
        return self.obj_file.filename

    @property
    def is_modified(self):
        return self.isModified()

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
            self.clear_indicators(Editor.WARNING_INDICATOR)
        else:
            self.checker = checker.Checker(self)
            self.connect(self.checker, SIGNAL("finished()"),
                         self._show_violations)

    def set_brace_matching(self):
        match_brace = int(settings.get_setting('editor/match-brace'))
        self.setBraceMatching(match_brace)

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
        current_line = settings.get_setting('editor/show-caret-line')
        self.send("sci_setcaretlinevisible", current_line)
        self.setEolVisibility(settings.get_setting('editor/eof'))

    def update_sidebar(self):
        """ Ajusta el ancho del sidebar """

        fmetrics = QFontMetrics(self._font)
        lines = str(self.lines()) + '0'
        line_number = settings.get_setting('editor/show-line-number')
        width = fmetrics.width(lines) if line_number else 0
        self.setMarginWidth(0, width)

    def show_line_numbers(self):
        line_number = settings.get_setting('editor/show-line-number')
        self.setMarginLineNumbers(0, line_number)
        self.update_sidebar()

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
        self._indentation = ancho

    def mark_words(self, palabras):
        self.clear_indicators(Editor.WORD_INDICATOR)
        for p in palabras:
            self.fillIndicatorRange(p[0], p[1], p[0], p[2],
                                    Editor.WORD_INDICATOR)

    def active_code_completion(self, enabled=True):
        if self.api is not None and enabled:
            return
        if enabled:
            self.api = QsciAPIs(self._lexer)
            if settings.get_setting('editor/completion-keywords'):
                for keyword in keywords.keywords:
                    self.api.add(keyword)
                self.api.prepare()
                source = QsciScintilla.AcsAPIs
                if settings.get_setting('editor/completion-document'):
                    source = QsciScintilla.AcsAll
            elif settings.get_setting('editor/completion-document'):
                source = QsciScintilla.AcsDocument
            else:
                source = QsciScintilla.AcsNone
            threshold = settings.get_setting('editor/completion-threshold')
            self.setAutoCompletionThreshold(threshold)
            self.setAutoCompletionSource(source)
            cs = settings.get_setting('editor/completion-cs')
            self.setAutoCompletionCaseSensitivity(cs)
            repl_word = settings.get_setting('editor/completion-replace-word')
            self.setAutoCompletionReplaceWord(repl_word)
            show_single = settings.get_setting('editor/completion-single')
            use_single = 2 if show_single else 0
            self.setAutoCompletionUseSingle(use_single)
        else:
            self.api = None
            self.setAutoCompletionSource(0)

    def _add_marker_modified(self):
        """ Agrega el marcador cuando el texto cambia """

        if not settings.get_setting('editor/mark-change'):
            return
        nline, _ = self.getCursorPosition()
        if self.markersAtLine(nline):
            self.markerDelete(nline)
        self.markerAdd(nline, Editor.MARKER_MODIFIED)

    def _show_violations(self):
        data = self.checker.data
        self.clear_indicators(Editor.WARNING_INDICATOR)
        for line, message in list(data.items()):
            line = int(line) - 1
            self.fillIndicatorRange(line, 0, line, self.lineLength(line),
                                    Editor.WARNING_INDICATOR)

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
                self.clear_indicators(Editor.WORD_INDICATOR)
                return
            self.search_thread.find(word, self.text())

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
        self.emit(SIGNAL("linesChanged(int)"), line)

    def keyPressEvent(self, event):
        super(Editor, self).keyPressEvent(event)
        key = event.key()
        # Borra indicador de palabra
        if key == Qt.Key_Escape:
            self.clear_indicators(Editor.WORD_INDICATOR)
            return
        # Completado de comillas
        if key == Qt.Key_Apostrophe:
            if settings.get_setting('editor/complete-single-quote'):
                self._complete_quote(event)
            return
        if key == Qt.Key_QuoteDbl:
            if settings.get_setting('editor/complete-double-quote'):
                self._complete_quote(event)
            return
        # Completado de llaves
        if key == Qt.Key_BraceLeft:
            if settings.get_setting('editor/complete-brace'):
                self._complete_key(event)
        if key in (Qt.Key_BracketLeft,
                   Qt.Key_ParenLeft,
                   Qt.Key_BracketRight,
                   Qt.Key_ParenRight):
            self._complete_brace(event)

    def _complete_quote(self, event):
        """ Autocompleta comillas simples y dobles, si existe el complementario
            el cursor se mueve un espacio.
        """

        complementary = Editor.QUOTE.get(event.text())
        line, index = self.getCursorPosition()
        text_line = self.text(line)
        portion = text_line[index - 1:index + 1]
        if portion in settings.QUOTES:
            self.setSelection(line, index, line, index + 1)
            self.replaceSelectedText('')
        else:
            self.insertAt(complementary, line, index)

    def _complete_brace(self, event):
        """ Autocompleta un brace cuando es abierto '(, ['.
            Si existe el complementario '), ]' el índice del cursor se
            mueve un espacio.
        """

        brace_close = settings.BRACES.get(event.text(), None)
        braces_open = list(Editor.BRACE.keys())
        line, index = self.getCursorPosition()
        if event.text() in settings.BRACES.values():
            text_line = self.text(line)
            found = 0
            # Busco un brace cerrado en el texto
            for token in text_line:
                if token in settings.BRACES.values():
                    found += 1
            try:
                # Brace abierto
                brace_open = text_line[index]
            except:
                brace_open = ''
            if found > 1 and brace_open not in braces_open:
                # Reemplazo el brace sobrante por un string vacío
                self.setSelection(line, index, line, index + 1)
                self.replaceSelectedText('')
            return
        elif event.text() in settings.BRACES.keys() and brace_close is not None:
            # Inserto el brace complementario
            self.insertAt(brace_close, line, index)

    def _complete_key(self, event):
        """ Autocompleta llaves en funciones y estructuras.
            Si se usa typedef en la definición de la estructura se completa
            la variable.
         """

        line, index = self.getCursorPosition()
        text_line = self.text(line)
        # Estructura
        if REGEX_STRUCT.match(text_line):
            if text_line.split()[0] == 'typedef':
                # Obtengo la variable
                split_line = text_line.split()
                if split_line[-1] == '{':
                    typedef = split_line[-2]
                else:
                    typedef = split_line[-1][:-1]
                text = "}%s;" % typedef.title()
            else:
                text = "};"
            self.insert("\n")
            self.insertAt(text, line + 1, 0)
            return
        # Función
        portion = text_line[index - 3: index]
        if ')' in portion:
            self.insert("\n")
            current_indentation = self.indentation(line)
            self.setIndentation(line + 1, current_indentation)
            self.insertAt('}', line + 1, current_indentation)

    def resizeEvent(self, e):
        super(Editor, self).resizeEvent(e)
        if self.minimap is not None:
            self.minimap.update_geometry()

    def comment(self):
        # FIXME: tener en cuenta /* */
        # FIXME: no funciona si el comentario no inicia en el índice 0
        if self.hasSelectedText():
            line_from, _, line_to, _ = self.getSelection()

            # Iterar todas las líneas seleccionadas
            self.send("sci_beginundoaction")
            for line in range(line_from, line_to + 1):
                self.insertAt('//', line, 0)
            self.send("sci_endundoaction")
        else:
            line, _ = self.getCursorPosition()
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
            linea, _ = self.getCursorPosition()
            self.indent(linea)

    def indent_less(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, _, hasta, _ = self.getSelection()
            for linea in range(desde, hasta + 1):
                self.unindent(linea)
            self.send("sci_endundoaction")
        else:
            linea, _ = self.getCursorPosition()
            self.unindent(linea)

    def move_down(self):
        self.send("sci_moveselectedlinesdown")

    def move_up(self):
        self.send("sci_moveselectedlinesup")

    def reemplazar_tabs_por_espacios(self):
        codigo = self.text()
        codigo_sin_tabs = codigo.replace('\t', ' ' * self._indentation)
        self.setText(codigo_sin_tabs)

    def saved(self):
        # Esta señal sirve para actualizar el árbol de símbolos
        self.emit(SIGNAL("fileSaved(QString)"), self.obj_file.filename)
        self.setModified(False)
        # Itera todas las líneas y si existe un _marker_modified agrega
        # un _marker_save
        for nline in range(self.lines()):
            if self.markersAtLine(nline):
                self.markerAdd(nline, Editor.MARKER_SAVED)

    def dropEvent(self, event):
        self.emit(SIGNAL("dropEvent(PyQt_PyObject)"), event)