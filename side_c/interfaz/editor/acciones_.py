#-*- coding: utf-8 -*-
from datetime import date
from datetime import datetime

from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPrintPreviewDialog
from PyQt4.QtGui import QApplication

comentario = '//'


def insertar_linea(ew):
    """ Inserta un una línea horizontal como separador. """

    ew.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    texto = ew.textCursor().selection().toPlainText()
    ew.moveCursor(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
    com = comentario * ((66 - len(texto)) / len(comentario))
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
        com = comentario * (30 / len(comentario))
        ew.textCursor().insertText(com)
        ew.textCursor().insertText(comentario + r)
        ew.textCursor().insertText(com)
        ew.textCursor().endEditBlock()


def insertar_fecha(ew):
    fecha = str(date.today())
    ew.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    ew.textCursor().insertText(fecha)
    ew.moveCursor(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)


def insertar_fecha_hora(ew):
    fecha_hora = str(datetime.now())
    ew.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    ew.textCursor().insertText(fecha_hora)
    ew.moveCursor(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)


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