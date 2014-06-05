#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c.interfaz.editor import acciones_
from side_c import recursos


class MenuInsertar(QObject):

    def __init__(self, menu_insertar, toolbar, ide):
        super(MenuInsertar, self).__init__()

        self.ide = ide

        accionTitulo = menu_insertar.addAction(
            QIcon(recursos.ICONOS['titulo']), self.trUtf8("Título"))
        accionTitulo.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
        accionSeparador = menu_insertar.addAction(
            QIcon(recursos.ICONOS['linea']), self.trUtf8("Separador"))
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

        # Conexión
        self.connect(accionSeparador, SIGNAL("triggered()"),
            self.insertar_separador)
        self.connect(accionTitulo, SIGNAL("triggered()"),
            self.insertar_titulo)
        accionDMA.triggered.connect(lambda x: self._insertar_fecha(1))
        accionMDA.triggered.connect(lambda x: self._insertar_fecha(2))
        accionAMD.triggered.connect(lambda x: self._insertar_fecha(3))
        accionDMAH.triggered.connect(lambda h: self._insertar_fecha_hora(1))
        accionMDAH.triggered.connect(lambda h: self._insertar_fecha_hora(2))
        accionAMDH.triggered.connect(lambda h: self._insertar_fecha_hora(3))

        # Toolbar
        self.items_toolbar = {
            "linea": accionSeparador,
            "titulo": accionTitulo
            }

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