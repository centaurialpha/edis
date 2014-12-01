# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QFont,
    QColor
    )

from PyQt4.QtCore import (
    pyqtSignal,
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


def crear_editor(nombre_archivo=''):
    ext = nombre_archivo.split('.')[-1]
    if not ext in recursos.EXTENSIONES:
        editor = Editor(nombre_archivo, ext)
        log.warning('Extensión no soportada')
    else:
        editor = Editor(nombre_archivo)
    return editor


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
            self.margen_de_linea(configuraciones.MARGEN_COLUMNA,
                                self._tema['margen'])
        # Brace matching
        self.match_braces(Base.SloppyBraceMatch)
        self.match_braces_color(self._tema['brace-background'],
                                self._tema['brace-foreground'])
        self.unmatch_braces_color(self._tema['brace-unbackground'],
                                    self._tema['brace-unforeground'])

        # Extras
        if configuraciones.GUIA_INDENTACION:
            self.setIndentationGuides(True)
            self.setIndentationGuidesBackgroundColor(QColor(
                                                    self._tema['guia-fondo']))
            self.setIndentationGuidesForegroundColor(QColor(
                                                    self._tema['guia-fore']))
        if configuraciones.MOSTRAR_TABS:
            self.setWhitespaceVisibility(self.WsVisible)

        # Conexión de señales
        self.connect(self, SIGNAL("modificationChanged(bool)"),
                    self.__modificado)
        self.connect(self, SIGNAL("textChanged()"),
                    self.__texto_cambiado)

    def devolver_posicion_del_cursor(self):
        """ Posición del cursor (línea, columna) """

        return self.getCursorPosition()

    def __modificado(self, estado):
        self._modificado.emit(estado)

    def __texto_cambiado(self):
        #FIXME: hago lo mismo en guardado()
        if not self.isUndoAvailable():
            self._undo.emit(self)
            self.nuevo_archivo = False
            self.texto_modificado = False

    def guardado(self, v=False):
        if not v:
            self._guardado.emit(self)
            self.nuevo_archivo = False
            self.texto_modificado = False
            self.setModified(self.texto_modificado)
