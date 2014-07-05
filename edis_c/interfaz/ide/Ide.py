#-*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL

from edis_c.interfaz.menu import menu_archivo
from edis_c.interfaz.menu import menu_editar
from edis_c.interfaz.menu import menu_ver
from edis_c.interfaz.menu import menu_insertar
from edis_c.interfaz.menu import menu_buscar
from edis_c.interfaz.menu import menu_codigo
from edis_c.interfaz.menu import menu_acerca_de

from edis_c.interfaz import widget_central
#from side_c.interfaz.contenedor_secundario import simbolos_widget
from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.contenedor_secundario import contenedor_secundario
from edis_c.interfaz import barra_de_estado

import edis_c
from edis_c import recursos
from edis_c.nucleo import configuraciones


ITEMS_TOOLBAR1 = [
    "nuevo-archivo",
    "abrir-archivo",
    "guardar-archivo",
    "separador",
    "deshacer",
    "rehacer",
    "separador",
    "cortar",
    "copiar",
    "pegar",
    "separador",
    "indentar",
    "desindentar",
    "include",
    "titulo",
    "linea",
    "separador"
    ]

ITEMS_TOOLBAR2 = [
    "compilar-archivo",
    "ejecutar-archivo",
    "compilar_ejecutar-archivo",
    "frenar"
    ]

__instanciaIde = None


# Singleton
def IDE(*args, **kw):
    global __instanciaIde
    if __instanciaIde is None:
        __instanciaIde = __IDE(*args, **kw)
    return __instanciaIde


class __IDE(QMainWindow):
    """ Aplicación principal """

    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(850, 700)
        self.setWindowTitle(edis_c.__nombre__)
        self._cargar_tema()
        get_pantalla = QDesktopWidget().screenGeometry()
        self.posicionar_ventana(get_pantalla)
        self.showMaximized()

        # Widget Central
        self.widget_Central = widget_central.WidgetCentral(self)
        self.cargar_ui(self.widget_Central)
        self.setCentralWidget(self.widget_Central)

        # ToolBar
        self.toolbar = QToolBar(self)
        self.toolbar_ = QToolBar(self)
        self.toolbar.setToolTip(self.trUtf8("Mantén presionado y mueve"))
        if not configuraciones.LINUX:
            self.toolbar_.setIconSize(QSize(25, 25))
            self.toolbar.setIconSize(QSize(25, 25))
        else:
            self.toolbar_.setIconSize(QSize(25, 25))
            self.toolbar.setIconSize(QSize(25, 25))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.addToolBar(Qt.RightToolBarArea, self.toolbar_)

        # Barra de estado
        self.barra_de_estado = barra_de_estado.BarraDeEstado(self)
        #self.barra_de_estado.hide()
        self.setStatusBar(self.barra_de_estado)

        # Menu
        menu = self.menuBar()
        archivo = menu.addMenu(self.tr("&Archivo"))
        editar = menu.addMenu(self.tr("&Editar"))
        ver = menu.addMenu(self.trUtf8("&Ver"))
        insertar = menu.addMenu(self.trUtf8("&Insertar"))
        buscar = menu.addMenu(self.trUtf8("&Buscar"))
        codigo = menu.addMenu(self.trUtf8("&Codigo fuente"))
        acerca = menu.addMenu(self.tr("Ace&rca de"))

        self._menu_archivo = menu_archivo.MenuArchivo(
            archivo, self.toolbar, self)
        self._menu_editar = menu_editar.MenuEditar(
            editar, self.toolbar_, self)
        self._menu_ver = menu_ver.MenuVer(ver, self)
        self._menu_insertar = menu_insertar.MenuInsertar(
            insertar, self.toolbar_, self)
        self._menu_buscar = menu_buscar.MenuBuscar(buscar, self)
        self._menu_codigo = menu_codigo.MenuCodigoFuente(
            codigo, self.toolbar, self)
        self._menu_acerca_de = menu_acerca_de.MenuAcercade(acerca, self)

        self.connect(self.contenedor_principal, SIGNAL("fileSaved(QString)"),
            self.mostrar_barra_de_estado)

        # Métodos para cargar items en las toolbar
        self.cargar_toolbar([self._menu_archivo, self._menu_editar,
            self._menu_insertar], self.toolbar, ITEMS_TOOLBAR1)

        self.cargar_toolbar([self._menu_codigo], self.toolbar_, ITEMS_TOOLBAR2)

        #if configuraciones.MOSTRAR_PAGINA_INICIO:
            #self.contenedor_principal.mostrar_pagina_de_inicio()

    def posicionar_ventana(self, pantalla):
        """ Posiciona la ventana en el centro de la pantalla. """

        tam_ventana = self.geometry()

        self.move((pantalla.width() - tam_ventana.width()) / 2,
                  (pantalla.height() - tam_ventana.height()) / 2)

    def cargar_ui(self, widget_central):
        self.contenedor_principal = contenedor_principal.ContenedorMain(self)
        self.contenedor_secundario = \
            contenedor_secundario.ContenedorBottom(self)

        self.connect(self.contenedor_principal, SIGNAL(
            "currentTabChanged(QString)"), self.cambiar_titulo_de_ventana)
        #self.widget_simbolos = simbolos_widget.SimbolosWidget()
        widget_central.agregar_contenedor_central(self.contenedor_principal)
        #widget_central.agregar_contenedor_lateral(self.widget_simbolos)
        widget_central.agregar_contenedor_bottom(self.contenedor_secundario)

        self.connect(self.contenedor_principal, SIGNAL(
            "cursorPositionChange(int, int)"), self._linea_columna)

    def cargar_toolbar(self, menus, toolbar, items):
        """ Carga los items en el toolbar
            menus: lista de menus o menu.
            toolbar: QToolBar
            items: lista de items
        """
        toolbar.clear()
        items_toolbar = {}

        if isinstance(menus, list):
            for menu in menus:
                items_toolbar.update(menu.items_toolbar)
        else:
            items_toolbar.update(menus.items_toolbar)

        for item in items:
            if item == 'separador':
                toolbar.addSeparator()
            else:
                item_tool = items_toolbar.get(item, None)

                if item_tool is not None:
                    toolbar.addAction(item_tool)

    def cargar_status_tips(self, accion, texto):
        accion.setStatusTip(texto)

    def cambiar_titulo_de_ventana(self, titulo):
        """ Cambia el título de la ventana cuando la pestaña cambia de nombre,
        esta emite la señal de cambio. """

        nombre_con_extension = os.path.basename(str(titulo)).split('/')[0]
        self.setWindowTitle(
            nombre_con_extension + ' (' + titulo + ')' + ' - EDIS-C')

    def _linea_columna(self):
        editor = self.contenedor_principal.devolver_editor_actual()
        if editor is not None:
            i = editor.textCursor().blockNumber() + 1
            j = editor.textCursor().columnNumber()
            self.barra_de_estado.linea_columna.actualizar_linea_columna(i, j)

    def closeEvent(self, evento):
        SI = QMessageBox.Yes
        CANCELAR = QMessageBox.Cancel

        if self.contenedor_principal.check_tabs_sin_guardar():
            v = QMessageBox.question(self,
                self.trUtf8("Algunos cambios no se han guardado"),
                (self.trUtf8("\n\n¿ Guardar los archivos ?")),
                SI, QMessageBox.No, CANCELAR)

            if v == SI:
                self.contenedor_principal.guardar_todo()

            if v == CANCELAR:
                evento.ignore()

    def mostrar_barra_de_estado(self, mensaje):
        self.barra_de_estado.show()
        self.barra_de_estado.showMessage(mensaje, 3000)

    def _cargar_tema(self):
        """ Carga el tema por defecto """

        qss = recursos.TEMA_POR_DEFECTO
        #qss = recursos.TEMA_BLACK_SIDE
        with open(qss) as q:
            tema = q.read()
        QApplication.instance().setStyleSheet(tema)