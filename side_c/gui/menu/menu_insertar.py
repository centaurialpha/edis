#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt


class MenuInsertar(QObject):

    def __init__(self, menu_insertar, ide):
        super(MenuInsertar, self).__init__()

        accionComentario = menu_insertar.addAction(self.trUtf8("Comentario"))
        accionComentario.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
        accionSeparador = menu_insertar.addAction(self.trUtf8("Separador"))
        accionSeparador.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)