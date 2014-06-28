#-*- coding: utf-8 -*-
import math

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QColor

from side_c import recursos

"""
Widget que muestra los números de líneas.
Basado en:
http://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
"""


class NumeroDeLineaBar(QWidget):

    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.editor = editor
        self.linea_superior = 0
        self.foldArea = 10
        self.negrita = False
        self._foldedBlocks = []

    def actualizar_area(self):
        linea_max = math.ceil(math.log10(self.editor.blockCount()))
        ancho = QFontMetrics(
            self.editor.document().defaultFont()).width('0' * int(linea_max)) \
            + 13 + self.foldArea
        if self.width() != ancho:
            self.setFixedWidth(ancho)
            self.editor.setViewportMargins(ancho, 0, 0, 0)
        self.actualizar()

    def code_folding_event(self, numerolinea):
        if self.is_folded(numerolinea):
            self.fold(numerolinea)

        else:
            self.unfold(numerolinea)

        self.editor.update()
        self.actualizar()

    def is_folded(self, linea):
        bloque = self.editor.document().findBlockByNumber(linea)
        if not bloque.isValid():
            return False
        return bloque.isVisible()

    def actualizar(self, *args):
        QWidget.update(self, *args)

    def paintEvent(self, event):
        fin_pagina = self.editor.viewport().height()
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        bloque_actual = self.editor.document().findBlock(
            self.editor.textCursor().position())

        pintar = QPainter(self)
        fondo = recursos.COLOR_EDITOR['widget-num-linea']
        pintar.fillRect(self.rect(), QColor(fondo))

        bloque = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        contar_linea = bloque.blockNumber()
        pintar.setFont(self.editor.document().defaultFont())

        while bloque.isValid():
            contar_linea += 1
            posicion = self.editor.blockBoundingGeometry(bloque).topLeft() + \
                viewport_offset

            if posicion.y() > fin_pagina:
                break

            pintar.setPen(QColor(recursos.COLOR_EDITOR['numero-linea']))

            if bloque == bloque_actual:
                self.negrita = True
                fuente = pintar.font()
                fuente.setBold(True)
                pintar.setFont(fuente)
                pintar.fillRect(
                    0, round(posicion.y()) + font_metrics.descent(),
                    self.width(),
                    font_metrics.ascent() + font_metrics.descent(),
                    QColor(recursos.COLOR_EDITOR['num-seleccionado']))

            if bloque.isVisible():
                pintar.drawText(self.width() - self.foldArea -
                font_metrics.width(str(contar_linea)) - 3,
                round(posicion.y()) + font_metrics.ascent() +
                font_metrics.descent() - 1,
                str(contar_linea))

            if self.negrita:
                fuente = pintar.font()
                fuente.setBold(False)
                pintar.setFont(fuente)

            bloque = bloque.next()

        self.linea_superior = contar_linea
        pintar.end()
        super(NumeroDeLineaBar, self).paintEvent(event)