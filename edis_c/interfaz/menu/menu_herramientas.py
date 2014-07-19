#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject

from edis_c import recursos
from edis_c.interfaz.editor import acciones_
from edis_c.interfaz.dialogos import dialogo_estadisticas


class MenuHerramientas(QObject):

    def __init__(self, menu_herramientas, toolbar, ide):
        super(MenuHerramientas, self).__init__()

        self.ide = ide

        # Acciones #
        # Insertar título
        accionTitulo = menu_herramientas.addAction(
            QIcon(recursos.ICONOS['titulo']), self.trUtf8("Insertar título"))
        # Insertar separador
        accionSeparador = menu_herramientas.addAction(
            QIcon(recursos.ICONOS['linea']), self.trUtf8("Insertar separador"))
        # Insertar include
        menu_include = menu_herramientas.addMenu(
            self.trUtf8("Insertar '#include'"))
        menu_libreria_estandar = menu_include.addMenu(
            self.trUtf8("Librería estándar"))
        accionStdio = menu_libreria_estandar.addAction(
            self.trUtf8("stdio.h"))
        accionStdlib = menu_libreria_estandar.addAction(
            self.trUtf8("stdlib.h"))
        accionString = menu_libreria_estandar.addAction(
            self.trUtf8("string.h"))
        accionInclude = menu_include.addAction(
            QIcon(recursos.ICONOS['insertar-include']),
            self.trUtf8("#include <...>"))
        menu_herramientas.addSeparator()
        # Insertar fecha y hora
        menu_fecha_hora = menu_herramientas.addMenu(
            self.trUtf8("Insertar fecha y hora"))
        accionDMA = menu_fecha_hora.addAction(
            self.trUtf8("dd-mm-aaaa"))
        accionMDA = menu_fecha_hora.addAction(
            self.trUtf8("mm-dd-aaaa"))
        accionAMD = menu_fecha_hora.addAction(
            self.trUtf8("aaaa-mm-dd"))
        menu_fecha_hora.addSeparator()
        accionDMAH = menu_fecha_hora.addAction(
            self.trUtf8("dd-mm-aaaa hh:mm"))
        accionMDAH = menu_fecha_hora.addAction(
            self.trUtf8("mm-dd-aaaa hh:mm"))
        accionAMDH = menu_fecha_hora.addAction(
            self.trUtf8("aaaa-mm-dd hh:mm"))
        menu_herramientas.addSeparator()
        self.accionEstadisticas = menu_herramientas.addAction(
            self.trUtf8("Estadísticas del documento"))

        # Toolbar #
        self.items_toolbar = {
            "linea": accionSeparador,
            "titulo": accionTitulo,
            "include": accionInclude
            }

        # Conexión
        accionSeparador.triggered.connect(self.insertar_separador)
        accionTitulo.triggered.connect(self.insertar_titulo)
        accionDMA.triggered.connect(lambda x: self._insertar_fecha(1))
        accionMDA.triggered.connect(lambda x: self._insertar_fecha(2))
        accionAMD.triggered.connect(lambda x: self._insertar_fecha(3))
        accionDMAH.triggered.connect(lambda h: self._insertar_fecha_hora(1))
        accionMDAH.triggered.connect(lambda h: self._insertar_fecha_hora(2))
        accionAMDH.triggered.connect(lambda h: self._insertar_fecha_hora(3))
        accionStdio.triggered.connect(lambda v: self._insertar_include(1))
        accionStdlib.triggered.connect(lambda v: self._insertar_include(2))
        accionString.triggered.connect(lambda v: self._insertar_include(3))
        accionInclude.triggered.connect(lambda v: self._insertar_include(4))
        self.accionEstadisticas.triggered.connect(
            self.estadisticas_del_documento)

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

    def estadisticas_del_documento(self):
        #editorW = self.ide.contenedor_principal.devolver_editor_actual()
        #if editorW and editorW.hasFocus():
            #dialogo_estadisticas.DialogoEstadisticas().show()
        self.ide.contenedor_principal.estadisticas()