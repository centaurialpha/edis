#-*- coding: utf-8 -*-

# <Widget Sidebar que muestra números de línea en el editor.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

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
import math

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPolygonF
from PyQt4.QtGui import QPixmap

from PyQt4.QtCore import QPointF
from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.interfaz.editor import acciones_

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
        self.foldArea = 20
        self.rightArrowIcon = QPixmap()
        self.downArrowIcon = QPixmap()
        self.negrita = False
        self.bloques_plegados = []
        self.pat = re.compile('(\s)*{|(\s)*#begin-fold:')

    def actualizar_area(self):
        linea_max = math.ceil(math.log10(self.editor.blockCount()))
        ancho = QFontMetrics(
            self.editor.document().defaultFont()).width('0' * int(linea_max)) \
            + 13 + self.foldArea
        if self.width() != ancho:
            self.setFixedWidth(ancho)
            self.editor.setViewportMargins(ancho, 0, 0, 0)
        self.actualizar()

    def evento_codigo_plegado(self, numerolinea):
        if self.se_pliega(numerolinea):
            self.plegar(numerolinea)

        else:
            self.desplegar(numerolinea)

        self.editor.update()
        self.actualizar()

    def plegar(self, lineNumber):
        inicio_bloque = self.editor.document().findBlockByNumber(lineNumber - 1)
        posicion_final = self._buscar_cierre_plegado(inicio_bloque)
        final_bloque = self.editor.document().findBlockByNumber(posicion_final)

        bloque = inicio_bloque.next()
        while bloque.isValid() and bloque != final_bloque:
            bloque.setVisible(False)
            bloque.setLineCount(0)
            bloque = bloque.next()

        self.bloques_plegados.append(inicio_bloque.blockNumber())
        self.editor.document().markContentsDirty(inicio_bloque.position(),
            posicion_final)

    def desplegar(self, lineNumber):
        inicio_bloque = self.editor.document().findBlockByNumber(lineNumber - 1)
        posicion_final = self._buscar_cierre_plegado(inicio_bloque)
        final_bloque = self.editor.document().findBlockByNumber(posicion_final)

        bloque = inicio_bloque.next()
        while bloque.isValid() and bloque != final_bloque:
            bloque.setVisible(True)
            bloque.setLineCount(bloque.layout().lineCount())
            posicion_final = bloque.position() + bloque.length()
            if bloque.blockNumber() in self.bloques_plegados:
                cierre = self._buscar_cierre_plegado(bloque)
                bloque = self.editor.document().findBlockByNumber(cierre)
            else:
                bloque = bloque.next()

        self.bloques_plegados.remove(inicio_bloque.blockNumber())
        self.editor.document().markContentsDirty(inicio_bloque.position(),
            posicion_final)

    def _buscar_cierre_plegado(self, bloque):
        texto = unicode(bloque.next())
        pat = re.compile('(\s)*#begin-fold:')
        patBrace = re.compile('(.)*{$')
        if pat.match(texto):
            return self._buscar_etiqueta_cierre_plegado(bloque)
        elif patBrace.match(texto):
            return self._buscar_cierre_llave_plegado(bloque)

        espacios = acciones_.devolver_espacios(texto)
        pat = re.compile('^\s*$|^\s*#')
        bloque = bloque.next()
        while bloque.isValid():
            texto2 = unicode(bloque.text())
            if not pat.match(texto2):
                final_espacio = acciones_.devolver_espacios(texto2)
                if len(final_espacio) <= len(espacios):
                    if pat.match(unicode(bloque.previous().text())):
                        return bloque.previous().blockNumber()
                    else:
                        return bloque.blockNumber()
            bloque = bloque.next()
        return bloque.previous().blockNumber()

    def _buscar_etiqueta_cierre_plegado(self, bloque):
        texto = unicode(bloque.next())
        label = texto.split(':')[0]
        bloque = bloque.next()
        pat = re.compile('\s*#end-fold:' + label)
        while bloque.isValid():
            if pat.match(unicode(bloque.next())):
                return bloque.blockNumber() + 1
            bloque = bloque.next()
        return bloque.blockNumber()

    def _buscar_cierre_llave_plegado(self, bloque):
        bloque = bloque.next()
        while bloque.isValid():
            llave_abierta = unicode(bloque.text()).count('{')
            llave_cerrada = unicode(bloque.text()).count('}') - llave_abierta
            if llave_cerrada > 0:
                return bloque.blockNumber() + 1
            bloque = bloque.next()
        return bloque.blockNumber()

    def se_pliega(self, linea):
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
        pattern = self.pat
        pintar = QPainter(self)
        fondo = QColor(recursos.NUEVO_TEMA.get('widget-num-lineas',
            recursos.TEMA_EDITOR['widget-num-linea']))
        fondo.setAlpha(40)
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

            pintar.setPen(QColor(recursos.NUEVO_TEMA.get('numero-linea',
                recursos.TEMA_EDITOR['numero-linea'])))

            if bloque == bloque_actual:
                self.negrita = True
                fuente = pintar.font()
                fuente.setBold(True)
                pintar.setFont(fuente)
                pintar.fillRect(
                    0, round(posicion.y()) + font_metrics.descent(),
                    self.width(),
                    font_metrics.ascent() + font_metrics.descent(),
                    QColor(recursos.NUEVO_TEMA.get('num-seleccionado',
                        recursos.TEMA_EDITOR['num-seleccionado'])))

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

        # Código desplegable
        area = self.width() - self.foldArea
        pintar.fillRect(area, 0, self.foldArea, self.height(),
            Qt.transparent)
        if self.foldArea != self.rightArrowIcon.width():
            poligono = QPolygonF()

            self.rightArrowIcon = QPixmap(self.foldArea, self.foldArea)
            self.rightArrowIcon.fill(Qt.transparent)
            self.downArrowIcon = QPixmap(self.foldArea, self.foldArea)
            self.downArrowIcon.fill(Qt.transparent)

            poligono.append(QPointF(self.foldArea * 0.5, self.foldArea * 0.25))
            poligono.append(QPointF(self.foldArea * 0.5, self.foldArea * 0.75))
            poligono.append(QPointF(self.foldArea * 0.8, self.foldArea * 0.5))
            iconPainter = QPainter(self.rightArrowIcon)
            iconPainter.setRenderHint(QPainter.Antialiasing)
            iconPainter.setPen(Qt.NoPen)
            iconPainter.setBrush(QColor(Qt.darkRed))
            iconPainter.drawPolygon(poligono)

            poligono.clear()
            poligono.append(QPointF(self.foldArea * 0.25, self.foldArea * 0.5))
            poligono.append(QPointF(self.foldArea * 0.75, self.foldArea * 0.5))
            poligono.append(QPointF(self.foldArea * 0.5, self.foldArea * 0.8))
            iconPainter = QPainter(self.downArrowIcon)
            iconPainter.setRenderHint(QPainter.Antialiasing)
            iconPainter.setPen(Qt.NoPen)
            iconPainter.setBrush(Qt.darkBlue)
            iconPainter.drawPolygon(poligono)

        bloque = self.editor.firstVisibleBlock()
        while bloque.isValid():
            posicion = self.editor.blockBoundingGeometry(
                bloque).topLeft() + viewport_offset

            if posicion.y() > fin_pagina:
                break

            if pattern.match(unicode(bloque.text())) and bloque.isValid():
                if bloque.blockNumber() in self.bloques_plegados:
                    pintar.drawPixmap(area, round(posicion.y()),
                        self.rightArrowIcon)
                else:
                    pintar.drawPixmap(area, round(posicion.y()),
                        self.downArrowIcon)
            bloque = bloque.next()
        pintar.end()
        QWidget.paintEvent(self, event)

    def mousePressEvent(self, event):
        if self.foldArea > 0:
            area = self.width() - self.foldArea
            font_metrics = QFontMetrics(self.editor.document().defaultFont())
            f = font_metrics.lineSpacing()
            y = event.posF().y()
            numero_linea = 0

            if event.pos().x() > area:
                patron = self.pat
                bloque = self.editor.firstVisibleBlock()
                viewport_offset = self.editor.contentOffset()
                fin_pagina = self.editor.viewport().height()

                while bloque.isValid():
                    posicion = self.editor.blockBoundingGeometry(
                        bloque).topLeft() + viewport_offset
                    if posicion.y() > fin_pagina:
                        break
                    if posicion.y() < y and (posicion.y() + f) > y and \
                        patron.match(str(bloque.text())):
                            numero_linea = bloque.blockNumber() + 1
                            break
                    bloque = bloque.next()
            if numero_linea > 0:
                self.evento_codigo_plegado(numero_linea)