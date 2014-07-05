#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt

from edis_c.interfaz.editor import acciones_
from edis_c import recursos


class MenuInsertar(QObject):

    def __init__(self, menu_insertar, toolbar, ide):
        super(MenuInsertar, self).__init__()

        self.ide = ide

        accionTitulo = menu_insertar.addAction(
            QIcon(recursos.ICONOS['titulo']), self.trUtf8("Título"))
        self.cargar_status_tip(accionTitulo,
            self.trUtf8("Insertar un título"))
        accionTitulo.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
        accionSeparador = menu_insertar.addAction(
            QIcon(recursos.ICONOS['linea']), self.trUtf8("Separador"))
        self.cargar_status_tip(accionSeparador,
            self.trUtf8("Insertar separador"))
        accionSeparador.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)
        menuFechaHora = menu_insertar.addMenu(
            self.trUtf8("Insertar fecha y hora"))
        accionDMA = menuFechaHora.addAction(
            self.trUtf8("dd-mm-aaaa"))
        accionMDA = menuFechaHora.addAction(
            self.trUtf8("mm-dd-aaaa"))
        accionAMD = menuFechaHora.addAction(
            self.trUtf8("aaaa-mm-dd"))
        menuFechaHora.addSeparator()
        accionDMAH = menuFechaHora.addAction(
            self.trUtf8("dd-mm-aaaa hh:mm"))
        accionMDAH = menuFechaHora.addAction(
            self.trUtf8("mm-dd-aaaa hh:mm"))
        accionAMDH = menuFechaHora.addAction(
            self.trUtf8("aaaa-mm-dd hh:mm"))
        menu_insertar.addSeparator()
        menuInclude = menu_insertar.addMenu(
            self.trUtf8("Insertar '#include <>'"))
        menuLibEst = menuInclude.addMenu(
            self.trUtf8("Libreria estandar"))
        accionStdIo = menuLibEst.addAction(
            self.trUtf8("stdio.h"))
        accionStdLib = menuLibEst.addAction(
            self.trUtf8("stdlib.h"))
        accionString = menuLibEst.addAction(
            self.trUtf8("string.h"))
        accionInclude = menuInclude.addAction(
            QIcon(recursos.ICONOS['insertar-include']),
            self.trUtf8("#include <...>"))

        # Conexión
        accionSeparador.triggered.connect(self.insertar_separador)
        accionTitulo.triggered.connect(self.insertar_titulo)
        accionDMA.triggered.connect(lambda x: self._insertar_fecha(1))
        accionMDA.triggered.connect(lambda x: self._insertar_fecha(2))
        accionAMD.triggered.connect(lambda x: self._insertar_fecha(3))
        accionDMAH.triggered.connect(lambda h: self._insertar_fecha_hora(1))
        accionMDAH.triggered.connect(lambda h: self._insertar_fecha_hora(2))
        accionAMDH.triggered.connect(lambda h: self._insertar_fecha_hora(3))
        accionStdIo.triggered.connect(lambda v: self._insertar_include(1))
        accionStdLib.triggered.connect(lambda v: self._insertar_include(2))
        accionString.triggered.connect(lambda v: self._insertar_include(3))
        accionInclude.triggered.connect(lambda v: self._insertar_include(4))

        # Toolbar
        self.items_toolbar = {
            "linea": accionSeparador,
            "titulo": accionTitulo,
            "include": accionInclude
            }

    def cargar_status_tip(self, accion, texto):
        self.ide.cargar_status_tips(accion, texto)

    def insertar_separador(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_linea(editorW)

    def insertar_titulo(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_titulo(editorW)

    def _insertar_fecha(self, formato):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_fecha(editorW, formato)

    def _insertar_fecha_hora(self, formato):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_fecha_hora(editorW, formato)

    def _insertar_include(self, valor):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_include(editorW, valor)