#-*- coding: utf-8 -*-8

# <Algunos métodos para el editor.>
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
import getpass
import socket
#from datetime import date
import datetime

from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPrintPreviewDialog
from PyQt4.QtGui import QApplication

from edis_c.nucleo import configuraciones

comentario_inicio = '/*'
comentario_fin = '*/'


def insertar_linea(ew):
    """ Inserta un una línea horizontal como separador. """

    #ew.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
   # texto = ew.textCursor().selection().toPlainText()
    #ew.moveCursor(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
    #com = comentario * ((66 - len(texto)) / len(comentario))
    com = comentario_inicio + ((configuraciones.MARGEN - 5) * '*') + \
        comentario_fin
    ew.textCursor().insertText(com)


def insertar_titulo(ew):
    """ Inserta un texto entre comentarios. """

    r = str(QInputDialog.getText(ew, ew.tr("Titulo"), ew.tr(
        "Ingresa el titulo:"))[0])
    if r:
        ew.textCursor().beginEditBlock()
        ew.moveCursor(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        com = comentario_inicio + (('*' * ((configuraciones.MARGEN - 10) / 2)))
        ew.textCursor().insertText(com)
        ew.textCursor().insertText(' ' + r + ' ')
        ew.textCursor().insertText(('*' * ((configuraciones.MARGEN - 10) / 2)))
        ew.textCursor().insertText(comentario_fin)
        ew.textCursor().endEditBlock()


def ir_a_linea_(editor):
    pass


def insertar_fecha(ew, formato):
    """ Inserta fecha formateada. """

    fecha = datetime.date.today()

    dicF = {
        1: "%d-%m-%Y",
        2: "%m-%d-%Y",
        3: "%Y-%m-%d"
        }

    for f in dicF:
        hoy = fecha.strftime(dicF.get(formato))

    ew.textCursor().insertText(hoy)


def insertar_fecha_hora(ew, formato):
    """ Inserta fecha y hora formateada. """

    fecha = datetime.datetime.now()
    dicF = {
        1: "%d-%m-%Y--%H:%M",
        2: "%m-%d-%Y--%H:%M",
        3: "%Y-%m-%d--%H:%M"
        }

    for f in dicF:
        hoy = fecha.strftime(dicF.get(formato))
    ew.textCursor().insertText(hoy)


def imprimir_archivo(nombre, f):
    """ Prepara el archivo para la impresión. """

    impres = QPrinter(QPrinter.HighResolution)
    impres.setPageSize(QPrinter.A4)
    impres.setOutputFileName(nombre)
    impres.setDocName(nombre)

    vista = QPrintPreviewDialog(impres)
    vista.paintRequested[QPrinter].connect(f)
    tam = QApplication.instance().desktop().screenGeometry()
    ancho = tam.width() - 100
    alto = tam.height() - 100
    vista.setMinimumSize(ancho, alto)
    vista.exec_()


def nuevo_main_c(ew):
    """ Inserta un texto con la función main. """

    nombre_usuario_equipo = obtener_user_hostname()
    ew.textCursor().insertText(
"""/*
 * <%s@%s>
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 *
 */


#include <stdio.h>

int main(int argc, char **argv)
{
    return 0;
}
""" % (nombre_usuario_equipo[0], nombre_usuario_equipo[1]))


def insertar_include(ew, libreria):
    """ Inserta alguna cabecera estándar o solo el include. """

    includes = {
        1: '#include <stdio.h>',
        2: '#include <stdlib.h>',
        3: '#include <string.h>',
        }

    if libreria != 3:
        for lib in includes:
            texto = includes.get(libreria)
        ew.textCursor().insertText(texto)

    #else:
        #texto = includes.get(4)
        #ew.textCursor().insertText(texto + '<>')
        #ew.moveCursor(QTextCursor.Left, QTextCursor.MoveAnchor)


def mover_hacia_arriba(editorW):
    """ Mueve hacia arriba una o más líneas seleccionadas. """

    cursor = editorW.textCursor()
    bloque_actual = cursor.block()
    if bloque_actual.blockNumber > 0:
        inicio = editorW.document().findBlock(
            cursor.selectionStart()).firstLineNumber()
        fin = editorW.document().findBlock(
            cursor.selectionEnd()).firstLineNumber()

        if cursor.hasSelection() and inicio != fin:
            pos_inicio = editorW.document().findBlockByLineNumber(
                inicio).position()
            cursor.setPosition(pos_inicio)
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor,
                fin - inicio)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            mover_texto = cursor.selectedText()
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.deleteChar()
            cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                QTextCursor.MoveAnchor)
            cursor.insertText(mover_texto + '\n')
            cursor.endEditBlock()
            pos_inicio = editorW.document().findBlockByLineNumber(
                (inicio - 1)).position()
            cursor.setPosition(pos_inicio)
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor,
                fin - inicio)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            editorW.setTextCursor(cursor)

        else:
            bloque_anterior = bloque_actual.previous()
            tmpLinea = str(bloque_actual.text())
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                QTextCursor.KeepAnchor)
            cursor.beginEditBlock()
            cursor.insertText(bloque_anterior.text())
            cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                QTextCursor.KeepAnchor)
            cursor.insertText(tmpLinea)
            cursor.endEditBlock()
            editorW.moveCursor(QTextCursor.Up, QTextCursor.MoveAnchor)


def mover_hacia_abajo(editorW):
    """ Mueve hacia abajo una o más lineas seleccionadas. """

    cursor = editorW.textCursor()
    bloque_actual = cursor.block()

    if bloque_actual.blockNumber() < (editorW.blockCount() - 1):
        inicio = editorW.document().findBlock(
            cursor.selectionStart()).firstLineNumber()
        fin = editorW.document().findBlock(
            cursor.selectionEnd()).firstLineNumber()

        if cursor.hasSelection() and inicio != fin:
            pos_inicio = editorW.document().findBlockByLineNumber(
                inicio).position()
            cursor.setPosition(pos_inicio)
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor,
                fin - inicio)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            mover_texto = cursor.selectedText()
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.deleteChar()
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.insertText('\n' + mover_texto)
            cursor.endEditBlock()
            pos_inicio = editorW.document().findBlockByLineNumber(
                (inicio - 1)).position()
            cursor.setPosition(pos_inicio)
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor,
                fin - inicio)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            editorW.setTextCursor(cursor)

        else:
            bloque_sig = bloque_actual.next()
            tmpLinea = str(bloque_actual.text())
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                QTextCursor.KeepAnchor)
            cursor.beginEditBlock()
            cursor.insertText(bloque_sig.text())
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine,
                QTextCursor.KeepAnchor)
            cursor.insertText(tmpLinea)
            cursor.endEditBlock()
            editorW.moveCursor(QTextCursor.Down, QTextCursor.MoveAnchor)


def ir_a_linea(Weditor):
    pass


def obtener_user_hostname():
    """ Devuelve una lista con el username y hostname. """

    usuario = getpass.getuser()
    equipo = socket.gethostname()
    return [usuario, equipo]


def devolver_espacios(linea):
    patIndentacion = re.compile('^\s+')
    espacio = patIndentacion.match(linea)

    if espacio is None:
        return ''
    return espacio.group()


def tabulaciones_por_espacios_en_blanco(Weditor):
    """ Reemplaza tabulaciones por espacios en blanco. """
    texto = Weditor.toPlainText()
    tabulacion = '\t'
    texto = texto.replace(tabulacion, ' ' * 4)
    Weditor.setPlainText(texto)


def convertir_a_mayusculas(Weditor):
    """ Convierte a mayúsculas un texto seleccionado o la línea en donde esta
    posicionado el cursor. """

    Weditor.textCursor().beginEditBlock()
    if Weditor.textCursor().hasSelection():
        texto = unicode(Weditor.textCursor().selectedText()).upper()
    else:
        texto = unicode(Weditor.texto_abajo()).upper()
        Weditor.moveCursor(QTextCursor.StartOfWord)
        Weditor.moveCursor(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
    Weditor.textCursor().insertText(texto)
    Weditor.textCursor().endEditBlock()


def convertir_a_minusculas(Weditor):
    """ Convierte a minúsculas un texto seleccionado o la línea en donde esta
    posicionado el cursor. """

    Weditor.textCursor().beginEditBlock()
    if Weditor.textCursor().hasSelection():
        texto = unicode(Weditor.textCursor().selectedText()).lower()
    else:
        texto = unicode(Weditor.texto_abajo()).lower()
        Weditor.moveCursor(QTextCursor.StartOfWord)
        Weditor.moveCursor(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
    Weditor.textCursor().insertText(texto)
    Weditor.textCursor().endEditBlock()


def convertir_a_titulo(Weditor):
    """ Convierte a tipo título un texto seleccionado o la línea en donde esta
    posicionado el cursor. """

    Weditor.textCursor().beginEditBlock()
    if Weditor.textCursor().hasSelection():
        texto = unicode(Weditor.textCursor().selectedText()).title()
    else:
        texto = unicode(Weditor.texto_abajo()).title()
        Weditor.moveCursor(QTextCursor.StartOfWord)
        Weditor.moveCursor(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
    Weditor.textCursor().insertText(texto)
    Weditor.textCursor().endEditBlock()


def eliminar_linea(Weditor):
    """ Elimina la línea en donde está posicionado el cursor. """

    cursor = Weditor.textCursor()
    cursor.beginEditBlock()

    cursor.select(QTextCursor.LineUnderCursor)
    cursor.removeSelectedText()
    cursor.deleteChar()

    cursor.endEditBlock()


def duplicar_linea(Weditor):
    """ Copia la línea en donde está posicionado el cursor y la inserta. """

    cursor = Weditor.textCursor()
    cursor.beginEditBlock()

    bloque = cursor.block()
    cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
    cursor.insertBlock()
    cursor.insertText(bloque.text())

    cursor.endEditBlock()


def comentar(Weditor):
    """ Comenta una (posición del cursor) o más lineas seleccionadas. """

    cursor = Weditor.textCursor()
    inicio_bloque = Weditor.document().findBlock(
        cursor.selectionStart())
    fin_bloque = Weditor.document().findBlock(
        cursor.selectionEnd()).next()
    cursor.beginEditBlock()

    while inicio_bloque != fin_bloque:
        cursor.setPosition(inicio_bloque.position())
        cursor.insertText('//')
        inicio_bloque = inicio_bloque.next()

    cursor.endEditBlock()


def descomentar(Weditor):
    """ Quita un (posición del cursor) o más lineas seleccionadas. """

    cursor = Weditor.textCursor()
    inicio_bloque = Weditor.document().findBlock(
        cursor.selectionStart())
    fin_bloque = Weditor.document().findBlock(
        cursor.selectionEnd()).next()
    cursor.beginEditBlock()

    while inicio_bloque != fin_bloque:
        posicion_comentario = unicode(inicio_bloque.text()).find('//')
        if unicode(inicio_bloque.text()).startswith(
            " " * posicion_comentario + '//'):
            cursor.setPosition(inicio_bloque.position() + posicion_comentario)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                len('//'))
            cursor.removeSelectedText()
        inicio_bloque = inicio_bloque.next()

    cursor.endEditBlock()


def ir_a_la_linea(Weditor):
    """ Posiciona el cursor en el número de línea que se ingresa. """

    maxim = Weditor.blockCount()
    linea = QInputDialog.getInt(Weditor, Weditor.tr("Ir a linea"),
        Weditor.tr("Linea:"), 1, 1, maxim, 1)
    print linea

    if linea[1]:
        if maxim >= linea[0]:
            cursor = Weditor.textCursor()
            cursor.setPosition(Weditor.document().findBlockByLineNumber(
                linea[0] - 1).position())
            Weditor.setTextCursor(cursor)
    Weditor.setFocus()


def quitar_espacios_en_blanco(editorWidget):
    cursor = editorWidget.textCursor()
    cursor.beginEditBlock()
    block = editorWidget.document().findBlockByLineNumber(0)
    while block.isValid():
        text = unicode(block.text())
        if text.endswith((' ', '\t')):
            cursor.setPosition(block.position())
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.insertText(text.rstrip())
        block = block.next()
    cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
    cursor.endEditBlock()