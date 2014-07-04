#-*- coding: utf-8 -*-8
#import re

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
    if not r:
        return None
    else:
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
    ew.textCursor().insertText(
"""/*
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
""")


def insertar_include(ew, libreria):
    includes = {
        1: '#include <stdio.h>',
        2: '#include <stdlib.h>',
        3: '#include <string.h>',
        4: '#include '
        }

    if libreria != 4:
        for lib in includes:
            texto = includes.get(libreria)
        ew.textCursor().insertText(texto)

    else:
        texto = includes.get(4)
        ew.textCursor().insertText(texto + '<>')