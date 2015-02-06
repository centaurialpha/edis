# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
from subprocess import Popen, PIPE
import os
import webbrowser
from collections import OrderedDict

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow,
    QIcon,
    QToolBar,
    QMessageBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    #SIGNAL,
    Qt,
    QSize,
    )

# Módulos EDIS
from src import ui
from src.ui import system_tray
from src.helpers import (
    configuracion,
    #dependencias
    )
from src.ui.widgets import tool_button
from src.helpers.configuracion import ESettings
from src.ui.dialogos import (
    dialogo_guardar_archivos,
    #dialogo_dependencias,
    acerca_de
    )


class EDIS(QMainWindow):
    """
    Esta clase es conocedora de todas las demás.

    """

    # Cada instancia de una clase  se guarda en éste diccionario
    __COMPONENTES = {}
    __LATERAL = {}  # Widgets laterales
    __MENUBAR = {}  # Nombre de los menus
    __ACCIONES = {}

    def __init__(self):
        QMainWindow.__init__(self)
        # Esto para tener widgets laterales en full height,
        # existe otra forma?
        window = QMainWindow(self)

        self.setWindowTitle(ui.__nombre__)
        self.setMinimumSize(750, 500)
        # Se cargan las dimensiones de la ventana
        d = ESettings.get('ventana/dimensiones')
        if d:
            self.resize(d)
        else:
            self.showMaximized()
        pos = ESettings.get('ventana/posicion')
        if pos != 0:
            self.move(pos)
        # Secciones del menubar
        EDIS.menu_bar(0, self.trUtf8("&Archivo"))
        EDIS.menu_bar(1, self.trUtf8("&Editar"))
        EDIS.menu_bar(2, self.trUtf8("&Ver"))
        EDIS.menu_bar(3, self.trUtf8("&Buscar"))
        EDIS.menu_bar(4, self.trUtf8("&Herramientas"))
        EDIS.menu_bar(5, self.trUtf8("E&jecución"))
        EDIS.menu_bar(6, self.trUtf8("A&cerca de"))
        # Toolbar
        self.toolbar = QToolBar(self)
        toggle_action = self.toolbar.toggleViewAction()
        toggle_action.setText(self.tr("Toolbar"))
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.dock_toolbar = QToolBar(self)
        toggle_action = self.dock_toolbar.toggleViewAction()
        toggle_action.setText(self.tr("Dock toolbar"))
        self.dock_toolbar.setObjectName("dock_toolbar")
        self.tb_simbolos = tool_button.CustomToolButton("Símbolos", self)
        self.tb_navegador = tool_button.CustomToolButton("Navegador", self)
        self.tb_explorador = tool_button.CustomToolButton("Explorador", self)
        self.dock_toolbar.setMovable(False)
        self.dock_toolbar.addWidget(self.tb_simbolos)
        self.dock_toolbar.addWidget(self.tb_navegador)
        self.dock_toolbar.addWidget(self.tb_explorador)
        self.addToolBar(Qt.LeftToolBarArea, self.dock_toolbar)
        # Animated property
        self.setDockOptions(QMainWindow.AnimatedDocks)
        # Menú
        self.cargar_menu()
        # Barra de estado
        self.barra_de_estado = EDIS.componente("barra_de_estado")
        self.setStatusBar(self.barra_de_estado)
        # Widget central
        central = self.cargar_central(window)
        window.setCentralWidget(central)
        window.setWindowFlags(Qt.Widget)
        self.setCentralWidget(window)

        EDIS.cargar_componente("edis", self)

        self.tb_simbolos.toggled.connect(self.toggled_simbolos)
        self.tb_navegador.toggled.connect(self.toggled_navegador)
        self.tb_explorador.toggled.connect(self.toggled_explorador)

        # Comprobar nueva versión
        self.noti = system_tray.NotificacionActualizacion()
        self.noti.show()

    @classmethod
    def cargar_componente(cls, nombre, instancia):
        """ Se guarda el nombre y la instancia de una clase """

        cls.__COMPONENTES[nombre] = instancia

    @classmethod
    def componente(cls, nombre):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTES.get(nombre, None)

    @classmethod
    def cargar_lateral(cls, nombre, instancia):
        cls.__LATERAL[nombre] = instancia

    @classmethod
    def lateral(cls, nombre):
        return cls.__LATERAL.get(nombre, None)

    @classmethod
    def menu_bar(cls, clave, nombre):
        """ Se guarda el nombre de cada menú """

        cls.__MENUBAR[clave] = nombre

    @classmethod
    def get_menu(cls, clave):
        """ Devuelve un diccionario con los menu """

        return cls.__MENUBAR.get(clave, None)

    @classmethod
    def accion(cls, nombre):
        return cls.__ACCIONES.get(nombre, None)

    def cargar_menu(self):
        #FIXME: Mejorar
        items_toolbar = OrderedDict()
        menu_bar = self.menuBar()
        menu_edis = self.componente("menu")
        principal = self.componente("principal")
        for i in range(7):
            menu = menu_bar.addMenu(self.get_menu(i))
            for accion in menu_edis.acciones:
                seccion = accion.seccion
                submenu = accion.submenu
                if seccion == i:
                    if submenu:
                        if isinstance(submenu, bool):
                            smenu = menu.addMenu(accion.nombre)
                            EDIS.__ACCIONES[accion.nombre] = smenu
                            if accion.nombre == 'Abrir reciente':
                                menu.addSeparator()
                            continue
                        else:
                            qaccion = smenu.addAction(accion.nombre)
                    else:
                        qaccion = menu.addAction(accion.nombre)
                    if accion.nombre in configuracion.ITEMS_TOOLBAR:
                        items_toolbar[accion.nombre] = qaccion
                    if accion.atajo:
                        qaccion.setShortcut(accion.atajo)
                    icono = accion.icono
                    if icono:
                        qaccion.setIcon(QIcon(icono))
                    if accion.conexion:
                        if accion.conexion.split('.')[0] == 'edis':
                            funcion = getattr(self,
                                              accion.conexion.split('.')[1],
                                              None)
                        else:
                            funcion = getattr(principal, accion.conexion, None)
                        # Es una función ?
                        if hasattr(funcion, '__call__'):
                            qaccion.triggered.connect(funcion)
                    if accion.separador:
                        menu.addSeparator()
                    EDIS.__ACCIONES[accion.nombre] = qaccion

        self.__cargar_toolbar(items_toolbar)

    def __cargar_toolbar(self, items_toolbar):
        #FIXME: Arreglar esto
        for i, accion in enumerate(list(items_toolbar.items())):
            if accion[0] in configuracion.ITEMS_TOOLBAR:
                self.toolbar.addAction(accion[1])
                if configuracion.ITEMS_TOOLBAR[i + 1] == 'separador':
                    self.toolbar.addSeparator()

    def cargar_central(self, window):
        principal = EDIS.componente("principal")
        start_page = False
        if ESettings.get('general/inicio'):
            principal.add_start_page()
            start_page = True
        self.simbolos = EDIS.lateral("simbolos")
        if start_page:
            self.simbolos.hide()
        self.navegador = EDIS.lateral("navegador")
        self.navegador.hide()
        self.explorador = EDIS.lateral("explorador")
        self.explorador.hide()
        self.output = EDIS.componente("output")
        window.addDockWidget(Qt.BottomDockWidgetArea, self.output)
        self.output.hide()
        for widget in [self.navegador, self.explorador, self.simbolos]:
            self.addDockWidget(Qt.LeftDockWidgetArea, widget)

        # Conexión
        self.simbolos.visibilityChanged[bool].connect(
            self.visibilidad_simbolos)
        self.navegador.visibilityChanged[bool].connect(
            self.visibilidad_navegador)
        self.explorador.visibilityChanged[bool].connect(
            self.visibilidad_explorador)
        principal.archivo_cambiado['QString'].connect(self.__actualizar_estado)
        principal.posicion_cursor.connect(self.__actualizar_cursor)
        principal.actualizarSimbolos['QString'].connect(
            self.simbolos.actualizar_simbolos)
        principal.archivo_cambiado['QString'].connect(
            self.simbolos.actualizar_simbolos)
        self.simbolos.irALinea[int].connect(principal.ir_a_linea)
        #FIXME: cambiar nombre
        self.output.salida_.output.ir_a_linea[int].connect(principal.ir_a_linea)
        principal.archivo_cambiado['QString'].connect(self.__titulo_ventana)
        principal.stack.todo_cerrado.connect(self.todo_cerrado)
        principal.stack.todo_cerrado.connect(principal.add_start_page)
        principal.archivo_abierto['QString'].connect(self.navegador.agregar)
        principal.archivo_cerrado[int].connect(self.navegador.eliminar)

        return principal

    #FIXME: mejorar
    def toggled_simbolos(self, t):
        if t:
            for w in [self.explorador, self.navegador]:
                w.hide()
            self.simbolos.show()
        else:
            self.simbolos.hide()

    def toggled_navegador(self, t):
        if t:
            for w in [self.explorador, self.simbolos]:
                w.hide()
            self.navegador.show()
        else:
            self.navegador.hide()

    def toggled_explorador(self, t):
        if t:
            for w in [self.navegador, self.simbolos]:
                w.hide()
            self.explorador.show()
        else:
            self.explorador.hide()

    def visibilidad_simbolos(self, v):
        self.tb_simbolos.setChecked(v)

    def visibilidad_navegador(self, v):
        self.tb_navegador.setChecked(v)

    def visibilidad_explorador(self, v):
        self.tb_explorador.setChecked(v)

    def __actualizar_cursor(self, linea, columna, lineas):
        self.barra_de_estado.cursor_widget.show()
        self.barra_de_estado.cursor_widget.actualizar_cursor(
            linea, columna, lineas)

    def __actualizar_estado(self, archivo):
        self.barra_de_estado.path_archivo(archivo)

    def todo_cerrado(self):
        self.setWindowTitle(ui.__nombre__)
        self.barra_de_estado.cursor_widget.hide()
        self.__actualizar_estado("")

    def __titulo_ventana(self, titulo):
        """ Cambia el título de la ventana (nombre_archivo - EDIS) """

        titulo = os.path.basename(titulo)
        self.setWindowTitle(titulo + ' - ' + ui.__nombre__)

    def reportar_bug(self):
        webbrowser.open_new(ui.__reportar_bug__)

    def mostrar_ocultar_output(self):
        if self.output.isVisible():
            self.output.hide()
        else:
            self.output.show()

    def mostrar_ocultar_toolbar(self):
        if self.toolbar.isVisible():
            self.toolbar.hide()
        else:
            self.toolbar.show()

    def mostrar_pantalla_completa(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cargar_archivos(self, archivos):
        """ Carga los archivos desde la última sesión """

        principal = EDIS.componente("principal")
        for archivo in archivos:
            principal.abrir_archivo(archivo[0], archivo[1])

    def acerca_de_qt(self):
        QMessageBox.aboutQt(self)

    def acerca_de_edis(self):
        dialogo = acerca_de.AcercaDe(self)
        dialogo.exec_()

    def closeEvent(self, e):
        """
        Éste médoto es llamado automáticamente por Qt cuando se
        cierra la aplicación

        """

        principal = EDIS.componente("principal")
        if principal.check_archivos_sin_guardar() and \
                ESettings.get('general/confirmarSalida'):

            archivos_sin_guardar = principal.archivos_sin_guardar()
            dialogo = dialogo_guardar_archivos.Dialogo(
                archivos_sin_guardar, principal)
            dialogo.exec_()
            if dialogo.ignorado():
                e.ignore()
        if ESettings.get('ventana/guardarDimensiones'):
            ESettings.set('ventana/dimensiones', self.size())
            ESettings.set('ventana/posicion', self.pos())
        ESettings.set('general/archivos', principal.archivos_abiertos())

    def detectar_dependencias(self):
        #FIXME: Mejorar
        pass
        #ok, ejec = dependencias.detectar()
        #if not ok:
            #dialogo = dialogo_dependencias.DialogoDependencias(ejec, self)
            #dialogo.show()

    def comprobar_compilador(self):
        #TODO: Quitar esto
        proceso = Popen('gcc --help', stdout=PIPE, stderr=PIPE, shell=True)
        if proceso.wait() != 0:
            flags = QMessageBox.Yes
            flags |= QMessageBox.No
            r = QMessageBox.warning(self,
                                    self.tr("No se encontro el compilador"),
                                    self.tr("Desea instalarlo?"), flags)
            if r == QMessageBox.Yes:
                self._descargar_compilador()
            elif r == QMessageBox.No:
                return False

    def _descargar_compilador(self):
        #FIXME:
        webbrowser.open_new(ui.__gcc__)

    def configuracion_edis(self):
        from src.ui.dialogos.preferencias import preferencias
        dialogo = preferencias.Preferencias(self)
        dialogo.show()
