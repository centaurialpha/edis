#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QInputDialog

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