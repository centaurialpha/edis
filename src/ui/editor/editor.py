# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

from PyQt4.QtGui import (
    QFont,
    QColor,
    )

from PyQt4.QtCore import (
    pyqtSignal,
    Qt,
    QThread,
    SIGNAL
    )

from src import recursos
from src.ui.editor.base import Base
from src.helpers import (
    configuraciones,
    logger
    )

# Logger
log = logger.edisLogger('editor')


def crear_editor(nombre_archivo):
    editor = Editor(nombre_archivo)
    log.debug('Se creó un nuevo editor: %s', nombre_archivo)
    return editor


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

    def __init__(self, nombre_archivo, ext='cpp'):
        super(Editor, self).__init__()
        self.texto_modificado = False
        self.nuevo_archivo = True
        self.guardado_actualmente = False
        self._palabra_seleccionada = ""

        # Thread ocurrencias
        self.hilo_ocurrencias = ThreadBusqueda()
        self.connect(self.hilo_ocurrencias,
                    SIGNAL("ocurrenciasThread(PyQt_PyObject)"),
                    self.marcar_palabras)
        # Lexer
        self.set_lexer(ext)
        # Fuente
        self.cargar_fuente(QFont(configuraciones.FUENTE,
                            configuraciones.TAM_FUENTE))
        self.setMarginsBackgroundColor(QColor(self._tema['sidebar-fondo']))
        self.setMarginsForegroundColor(QColor(self._tema['sidebar-fore']))

        # Línea actual, cursor
        self.caret_line(self._tema['caret-background'],
                        self._tema['caret-line'], self._tema['caret-opacidad'])

        # Márgen
        if configuraciones.MARGEN:
            self._margen_de_linea(configuraciones.MARGEN_COLUMNA)

        # Brace matching
        self.match_braces(Base.SloppyBraceMatch)
        self.match_braces_color(self._tema['brace-background'],
                                self._tema['brace-foreground'])
        self.unmatch_braces_color(self._tema['brace-unbackground'],
                                    self._tema['brace-unforeground'])

    def flags(self):
        """ Extras para el editor """

        if configuraciones.MOSTRAR_TABS:
            self.setWhitespaceVisibility(self.WsVisible)
        else:
            self.setWhitespaceVisibility(self.WsInvisible)
        self.setIndentationGuides(configuraciones.GUIA_INDENTACION)
        if configuraciones.GUIA_INDENTACION:
            self.setIndentationGuidesBackgroundColor(QColor(
                                                    self._tema['guia-fondo']))
            self.setIndentationGuidesForegroundColor(QColor(
                                                    self._tema['guia-fore']))
        if configuraciones.MODO_ENVOLVER:
            self.setWrapMode(self.WrapWord)
        else:
            self.setWrapMode(self.WrapNone)

    def devolver_posicion_del_cursor(self):
        """ Posición del cursor (línea, columna) """

        return self.getCursorPosition()

    def _margen_de_linea(self, margen=None):
        if configuraciones.MARGEN:
            self.setEdgeMode(Base.EdgeLine)
            self.setEdgeColumn(margen)
            self.setEdgeColor(QColor(self._tema['margen']))
        else:
            self.setEdgeMode(Base.EdgeNone)

    def marcar_palabras(self, palabras):
        self.borrarIndicadores(self.indicador)
        for p in palabras:
            self.fillIndicatorRange(p[0], p[1], p[0], p[2], self.indicador)

    def busqueda(self, palabra, re=False, cs=False, wo=False, wrap=True,
                forward=True):
        pass

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

    def keyPressEvent(self, e):
        super(Editor, self).keyPressEvent(e)
        if e.key() == Qt.Key_Escape:
            self.borrarIndicadores(self.indicador)

    def guardado(self):
        self._guardado.emit(self)
        self.nuevo_archivo = False
        self.texto_modificado = False