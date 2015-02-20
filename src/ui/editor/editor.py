# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

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
#from PyQt4.Qsci import (
    #QsciScintilla,
    #QsciAPIs
    #)

from src import recursos
from src.ui.editor.base import Base
from src.ui.editor.minimapa import MiniMapa
from src.ui.editor import (
    checker,
    lexer,
    #keywords
    )
from src.helpers.configuracion import ESettings

#FIXME: Cambiar comentario '//' (C++ style) por '/* */' (C style)


class ThreadBusqueda(QThread):
    """ Éste hilo busca ocurrencias de una palabra en el código fuente """

    def run(self):
        palabra = re.escape(self.__palabra)
        encontradas = []
        linea = 0

        for linea_texto in self.__codigo.splitlines():
            indice = linea_texto.find(palabra)
            if indice != -1:
                indice_start = indice
                indice_end = indice_start + len(palabra)
                encontradas.append([linea, indice_start, indice_end])
            linea += 1
        self.emit(SIGNAL("ocurrenciasThread(PyQt_PyObject)"), encontradas)

    def buscar(self, palabra, codigo):
        self.__codigo = codigo
        self.__palabra = palabra

        # Run!
        self.start()


class Editor(Base):

    # Estilo
    _tema = recursos.TEMA

    # Señales
    _modificado = pyqtSignal(bool, name='archivo_modificado')
    _guardado = pyqtSignal(['PyQt_PyObject'], name='archivo_guardado')
    _undo = pyqtSignal(['PyQt_PyObject'], name='accion_undo')
    _drop = pyqtSignal(['PyQt_PyObject'], name='dropSignal')

    def __init__(self):
        super(Editor, self).__init__()
        self.__nombre = ""
        self.texto_modificado = False
        self.es_nuevo = True
        self.guardado_actualmente = False
        # Actualiza flags (espacios en blanco, cursor, sidebar, etc)
        self.actualizar()
        # Lexer
        self._lexer = lexer.Lexer()
        self.setLexer(self._lexer)
        # Autocompletado
        #FIXME: autocompeltado
        #api = QsciAPIs(self._lexer)
        #for palabra in keywords.keywords:
            #api.add(palabra)
        #api.prepare()
        #self.setAutoCompletionThreshold(1)
        #self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        # Indentación
        self._indentacion = ESettings.get('editor/indentacionAncho')
        self.send("sci_settabwidth", self._indentacion)
        # Minimapa
        self.minimapa = MiniMapa(self)
        self.connect(self, SIGNAL("selectionChanged()"), self.minimapa.area)
        self.connect(self, SIGNAL("textChanged()"),
                     self.minimapa.actualizar_codigo)
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
        fuente = ESettings.get('editor/fuente')
        tam_fuente = ESettings.get('editor/fuenteTam')
        self.cargar_fuente(fuente, tam_fuente)
        self.setMarginsBackgroundColor(QColor(self._tema['sidebar-fondo']))
        self.setMarginsForegroundColor(QColor(self._tema['sidebar-fore']))

        # Línea actual, cursor
        self.caret_line(self._tema['caret-background'],
                        self._tema['caret-line'], self._tema['caret-opacidad'])
        # Márgen
        if ESettings.get('editor/margen'):
            self.actualizar_margen()

        # Brace matching
        self.match_braces(Base.SloppyBraceMatch)
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
            self.borrarIndicadores(self.indicador_warning)
        else:
            self.checker = checker.Checker(self)
            self.connect(self.checker, SIGNAL("finished()"),
                         self._show_violations)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):  # lint:ok
        self.__nombre = nuevo_nombre
        if nuevo_nombre:
            self.es_nuevo = False
        if self.checker is not None:
            self.checker.start_checker()

    def actualizar(self):
        """ Actualiza las opciones del editor """

        if ESettings.get('editor/mostrarTabs'):
            self.setWhitespaceVisibility(self.WsVisible)
        else:
            self.setWhitespaceVisibility(self.WsInvisible)
        self.setIndentationGuides(ESettings.get('editor/guias'))
        if ESettings.get('editor/guias'):
            self.setIndentationGuidesBackgroundColor(QColor(
                                                     self._tema['guia-fondo']))
            self.setIndentationGuidesForegroundColor(QColor(
                                                     self._tema['guia-fore']))
        if ESettings.get('editor/modoWrap'):
            self.setWrapMode(self.WrapWord)
        else:
            self.setWrapMode(self.WrapNone)
        self.send("sci_setcaretstyle", ESettings.get('editor/tipoCursor'))

    @property
    def altura_lineas(self):
        linea, i = self.devolver_posicion_del_cursor()
        return self.textHeight(linea)

    def devolver_posicion_del_cursor(self):
        """ Posición del cursor (línea, columna) """

        return self.getCursorPosition()

    def actualizar_margen(self):
        """ Actualiza el ancho del márgen de línea """

        if ESettings.get('editor/margen'):
            self.setEdgeMode(Base.EdgeLine)
            ancho = ESettings.get('editor/margenAncho')
            self.setEdgeColumn(ancho)
            self.setEdgeColor(QColor(self._tema['margen']))
        else:
            self.setEdgeMode(Base.EdgeNone)

    def actualizar_indentacion(self):
        ancho = ESettings.get('editor/indentacionAncho')
        self.send("sci_settabwidth", ancho)
        self._indentacion = ancho

    def marcar_palabras(self, palabras):
        self.borrarIndicadores(self.indicador)
        for p in palabras:
            self.fillIndicatorRange(p[0], p[1], p[0], p[2], self.indicador)

    def _show_violations(self):
        data = self.checker.data
        self.borrarIndicadores(self.indicador_warning)
        for line, message in list(data.items()):
            line = int(line) - 1
            self.fillIndicatorRange(line, 0, line, self.lineLength(line),
                                    self.indicador_warning)

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

        #FIXME: Marcar palabras encontradas
        if self.hasSelectedText():
            linea, indice, lhasta, ihasta = self.getSelection()
        if wrap:
            linea, indice = -1, -1
        self.findFirst(palabra, re, cs, wo, wrap, forward, linea, indice)

    def reemplazar(self, reemplazar, reemplazo, todo=False):
        """ Reemplaza una o varias ocurrencias de @reemplazar por @reemplazo """

        #FIXME: posición del cursor
        self.send("sci_beginundoaction")
        if self.hasSelectedText():
            self.replaceSelectedText(reemplazo)
        while todo:
            ok = self.findNext()
            if not ok:
                break
            self.replace(reemplazo)
        self.send("sci_endundoaction")

    def _texto_bajo_el_cursor(self):
        """ Texto seleccionado con el cursor """

        linea, indice = self.getCursorPosition()  # Posición del cursor
        palabra = self.wordAtLineIndex(linea, indice)  # Palabra en esa pos
        return palabra

    def mouseReleaseEvent(self, e):
        super(Editor, self).mouseReleaseEvent(e)
        if e.button() == Qt.LeftButton:
            self.hilo_ocurrencias.buscar(
                self._texto_bajo_el_cursor(), self.texto)

    def mouseMoveEvent(self, event):
        super(Editor, self).mouseMoveEvent(event)
        if self.checker is None:
            return
        position = event.pos()
        line = str(self.lineAt(position) + 1)
        message = self.checker.data.get(line, None)
        if message is not None:
            QToolTip.showText(self.mapToGlobal(position), message)

    def keyPressEvent(self, e):
        super(Editor, self).keyPressEvent(e)
        if e.key() == Qt.Key_Escape:
            self.borrarIndicadores(self.indicador)
        if e.key() == Qt.Key_BraceLeft:
            #FIXME: autocompletar llave
            pass

    def resizeEvent(self, e):
        super(Editor, self).resizeEvent(e)
        self.minimapa.redimensionar()

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

    def a_titulo(self):
        #FIXME: Tratar cuando no se selecciona texto
        self.send("sci_beginundoaction")
        if self.hasSelectedText():
            texto = self.selectedText().title()
        self.replaceSelectedText(texto)
        self.send("sci_endundoaction")

    def duplicar_linea(self):
        self.send("sci_lineduplicate")

    def eliminar_linea(self):
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

    def indentar(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, _, hasta, _ = self.getSelection()
            for linea in range(desde, hasta + 1):
                self.indent(linea)
            self.send("sci_endundoaction")
        else:
            linea, _ = self.devolver_posicion_del_cursor()
            self.indent(linea)

    def quitar_indentacion(self):
        if self.hasSelectedText():
            self.send("sci_beginundoaction")
            desde, _, hasta, _ = self.getSelection()
            for linea in range(desde, hasta + 1):
                self.unindent(linea)
            self.send("sci_endundoaction")
        else:
            linea, _ = self.devolver_posicion_del_cursor()
            self.unindent(linea)

    def mover_linea_abajo(self):
        self.send("sci_moveselectedlinesdown")

    def mover_linea_arriba(self):
        self.send("sci_moveselectedlinesup")

    def _completar_brace(self, e):
        #FIXME: Evitar duplicar brace
        braces = {'{': '}', '(': ')', '[': ']'}
        brace = e.text()
        complementario = braces.get(brace)
        linea, indice = self.devolver_posicion_del_cursor()
        self.insertAt(complementario, linea, indice + 1)

    def guardado(self):
        self._guardado.emit(self)
        self.es_nuevo = False
        self.texto_modificado = False

    def dropEvent(self, evento):
        self._drop.emit(evento)