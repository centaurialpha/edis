#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c.gui.editor import acciones_


class MenuInsertar(QObject):

    def __init__(self, menu_insertar, ide):
        super(MenuInsertar, self).__init__()

        self.ide = ide

        accionComentario = menu_insertar.addAction(self.trUtf8("Título"))
        accionComentario.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
        accionSeparador = menu_insertar.addAction(self.trUtf8("Separador"))
        accionSeparador.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)

        self.connect(accionSeparador, SIGNAL("triggered()"),
            self.insertar_separador)
        self.connect(accionComentario, SIGNAL("triggered()"),
            self.insertar_titulo)

    def insertar_separador(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_linea(editorW)

    def insertar_titulo(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_titulo(editorW)