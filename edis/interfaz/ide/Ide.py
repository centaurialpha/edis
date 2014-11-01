#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

# Módulos Python
import os
import sys
from re import findall
from subprocess import Popen, PIPE

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow,
    QDesktopWidget,
    QToolBar,
    QApplication,
    QMessageBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    Qt,
    QSize,
    SIGNAL,
    QSettings
    )

# Módulos EDIS
from edis import interfaz
from edis import recursos
from edis.nucleo import configuraciones
from edis.interfaz import actualizaciones
from edis.interfaz.menu import (
    menu_archivo,
    menu_editar,
    menu_ver,
    menu_buscar,
    menu_herramientas,
    menu_ejecucion,
    menu_acerca_de
    )
from edis.interfaz import widget_central
from edis.interfaz.distribuidor import Distribuidor
from edis.interfaz.contenedor_principal import contenedor_principal
from edis.interfaz.contenedor_secundario import contenedor_secundario
from edis.interfaz.lateral_widget import lateral_container
from edis.interfaz.widgets import barra_de_estado
from edis.interfaz.dialogos import dialogo_guardar_archivos


class IDE(QMainWindow):
    """ Aplicación principal """

    instancia = None

    def __new__(cls, *args, **kargs):
        if cls.instancia is None:
            cls.instancia = QMainWindow.__new__(cls, *args, **kargs)
        return cls.instancia

    def __init__(self):
        QMainWindow.__init__(self)
        self.ini = False
        self.setMinimumSize(850, 700)
        self.setWindowTitle(interfaz.__nombre__)
        self.comprobar_compilador()
        self._cargar_tema()
        get_pantalla = QDesktopWidget().screenGeometry()
        self.posicionar_ventana(get_pantalla)
        self.showMaximized()

        # Distribuidor
        self.distribuidor = Distribuidor()
        # Widget Central
        self.widget_Central = widget_central.WidgetCentral(self)
        self.cargar_ui(self.widget_Central)
        self.setCentralWidget(self.widget_Central)
        # ToolBar
        self.toolbar = QToolBar(self)
        self.toolbar_busqueda = QToolBar(self)
        #self.toolbar_busqueda.addWidget(line_busqueda.Widget())
        self.toolbar_busqueda.setMovable(False)
        self.toolbar.setToolTip(self.trUtf8("Mantén presionado y mueve"))

        # Tamaño de íconos de barra de herramientas
        self.toolbar.setIconSize(QSize(20, 20)) if not configuraciones.LINUX \
            else self.toolbar.setIconSize(QSize(19, 19))

        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar_busqueda)

        self.tray = actualizaciones.Actualizacion(self)
        self.tray.show()
        # Barra de estado
        self.barra_de_estado = barra_de_estado.BarraDeEstado(self)
        #self.barra_de_estado.hide()
        self.setStatusBar(self.barra_de_estado)
        # Menu
        menu = self.menuBar()
        archivo = menu.addMenu(self.tr("&Archivo"))
        editar = menu.addMenu(self.tr("&Editar"))
        ver = menu.addMenu(self.trUtf8("&Ver"))
        buscar = menu.addMenu(self.trUtf8("&Buscar"))
        herramientas = menu.addMenu(self.trUtf8("&Herramientas"))
        ejecucion = menu.addMenu(self.trUtf8("E&jecucion"))
        acerca = menu.addMenu(self.tr("Ace&rca de"))
        self._menu_archivo = menu_archivo.MenuArchivo(
            archivo, self.toolbar, self)
        self._menu_editar = menu_editar.MenuEditar(
            editar, self.toolbar, self)
        self._menu_ver = menu_ver.MenuVer(ver, self.toolbar, self)
        self._menu_herramientas = menu_herramientas.MenuHerramientas(
            herramientas, self.toolbar, self)
        self._menu_buscar = menu_buscar.MenuBuscar(buscar, self.toolbar, self)
        self._menu_ejecucion = menu_ejecucion.MenuEjecucion(
            ejecucion, self.toolbar, self)
        self._menu_acerca_de = menu_acerca_de.MenuAcercade(acerca, self)

        self.connect(self.contenedor_principal,
            SIGNAL("recentTabsModified(QStringList)"),
            self._menu_archivo.actualizar_archivos_recientes)
        self.connect(self._menu_archivo, SIGNAL("abrirArchivo(QString)"),
            self.contenedor_principal.abrir_archivo)
        self.connect(self.contenedor_principal,
            SIGNAL("currentTabChanged(QString)"),
            self.lateral.actualizar_simbolos)
        # Método para cargar items en las toolbar
        self.cargar_toolbar()

        if configuraciones.PAGINA_BIENVENIDA:
            self.contenedor_principal.mostrar_pagina_de_bienvenida()
        # Iniciar distribuidor despues de la interfáz
        #FIXME: arreglar !!
        self.distribuidor.ini_ide(self)
        self.ini = True

    def posicionar_ventana(self, pantalla):
        """ Posiciona la ventana en el centro de la pantalla. """

        tam_ventana = self.geometry()

        self.move((pantalla.width() - tam_ventana.width()) / 2,
                  (pantalla.height() - tam_ventana.height()) / 2)

    def cargar_ui(self, widget_central):
        """ Carga los contenedores. """

        self.contenedor_principal = contenedor_principal.ContenedorMain(self)
        self.contenedor_secundario = \
            contenedor_secundario.ContenedorSecundario(self)
        self.lateral = lateral_container.LateralContainer(self)
        self.connect(self.contenedor_principal,
            SIGNAL("desactivarBienvenida()"),
            self.desactivar_pagina_de_bienvenida)
        self.connect(self.contenedor_principal, SIGNAL(
            "currentTabChanged(QString)"), self.cambiar_titulo_de_ventana)
        self.connect(self.contenedor_principal, SIGNAL(
            "currentTabChanged(QString)"), self.cambiar_barra_estado)
        self.connect(self.contenedor_principal, SIGNAL("nuevoArchivo()"),
            self.contenedor_principal.agregar_editor)
        self.connect(self.contenedor_principal, SIGNAL("abrirArchivo()"),
            self.contenedor_principal.abrir_archivo)

        widget_central.agregar_contenedor_central(self.contenedor_principal)
        widget_central.agregar_contenedor_bottom(self.contenedor_secundario)
        widget_central.agregar_contenedor_lateral(self.lateral)

        self.connect(self.lateral.symbols_widget,
            SIGNAL("infoSimbolo(QString)"),
            widget_central.lateral.set_info_simbolo)
        self.connect(self.contenedor_principal, SIGNAL(
            "actualizarSimbolos(QString)"), self.lateral.actualizar_simbolos)
        self.connect(self.contenedor_principal, SIGNAL(
            "cursorPositionChange(int, int)"), self._linea_columna)
        #FIXME: quitar función lambda
        self.connect(self.lateral.file_navigator, SIGNAL("cambioPes(int)"),
            lambda i: self.contenedor_principal.tab.setCurrentIndex(i))
        self.connect(self.lateral.file_explorer,
            SIGNAL("dobleClickArchivo(QString)"),
            lambda f: self.contenedor_principal.abrir_archivo(f))

    def desactivar_pagina_de_bienvenida(self):
        """ Desactiva la página de inicio al iniciar próxima sesión. """

        configuraciones.PAGINA_BIENVENIDA = False
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        qconfig.setValue('configuraciones/general/paginaBienvenida',
            configuraciones.PAGINA_BIENVENIDA)
        self.contenedor_principal.tab_actual.cerrar_tab()

    def cargar_toolbar(self):
        self.toolbar.clear()
        items = {}

        items.update(self._menu_archivo.items_toolbar)
        items.update(self._menu_editar.items_toolbar)
        items.update(self._menu_buscar.items_toolbar)
        #items.update(self._menu_ver.items_toolbar)
        #items.update(self._menu_herramientas.items_toolbar)
        items.update(self._menu_ejecucion.items_toolbar)
        for i in configuraciones.BARRA_HERRAMIENTAS_ITEMS:
            if i == 'separador':
                self.toolbar.addSeparator()
            else:
                item = items.get(i, None)
                if item is not None:
                    #self.toolbar.addAction(item)
                    self.toolbar.addWidget(item)

    def cargar_status_tips(self, accion, texto):
        accion.setStatusTip(texto)

    def cambiar_barra_estado(self, archivo):
        self.barra_de_estado.nombre_archivo.cambiar_texto(archivo)

    def cambiar_titulo_de_ventana(self, titulo):
        """ Cambia el título de la ventana cuando la pestaña cambia de nombre,
        esta emite la señal de cambio. """

        if titulo == interfaz.__nombre__:
            titulo = ""
            return

        nombre_con_extension = os.path.basename(str(titulo)).split('/')[0]
        self.setWindowTitle(nombre_con_extension + ' - ' + interfaz.__nombre__)

    def _linea_columna(self):
        """ Muestra el número de línea y columna del archivo actual. """

        editor = self.contenedor_principal.devolver_editor_actual()
        if editor is not None:
            linea = editor.textCursor().blockNumber() + 1
            columna = editor.textCursor().columnNumber()
            total_lineas = editor.devolver_cantidad_de_lineas()
            self.barra_de_estado.estado_cursor.actualizar_posicion_cursor(
                linea, total_lineas, columna)

    def keyPressEvent(self, evento):
        pass

    def closeEvent(self, evento):
        """ Al cerrar EDIS se comprueba archivos no guardados y se guardan
        las configuraciones. """

        if self.contenedor_principal.check_tabs_sin_guardar() and \
        configuraciones.CONFIRMAR_AL_CERRAR:
            archivos_sin_guardar = \
                self.contenedor_principal.devolver_archivos_sin_guardar()
            dialogo = dialogo_guardar_archivos.Dialogo(archivos_sin_guardar)
            dialogo.exec_()
            if dialogo.ignorado():
                evento.ignore()
        self.guardar_configuraciones()

    def _cargar_tema(self):
        """ Carga el tema por defecto """

        with open(recursos.TEMA_POR_DEFECTO) as q:
            tema = q.read()
        QApplication.instance().setStyleSheet(tema)

    def cargar_sesion(self, archivosPrincipales, archivos_recientes=None):
        """ Carga archivos desde la última sesión. """

        self.contenedor_principal.abrir_archivos(archivosPrincipales)
        if archivos_recientes:
            self._menu_archivo.actualizar_archivos_recientes(archivos_recientes)

    def comprobar_compilador(self):
        """ Antes de cargar la interfáz de EDIS se comprueba si GCC está
        presente en el sistema. """

        sistema = sys.platform
        execs = {'Win': True if not sistema else False}
        discos_win = findall(r'(\w:)\\',
            Popen('fsutil fsinfo drives', stdout=PIPE).communicate()[0]) if \
                execs['Win'] else None
        progs = ['gcc']
        progs = [progs] if isinstance(progs, str) else progs
        for prog in progs:
            if execs['Win']:  # Comprobación en Windows
                win_cmds = ['dir /B /S {0}\*{1}.exe'.format(letter, prog) for
                            letter in discos_win]
                for cmd in win_cmds:
                    execs[prog] = (Popen(cmd, stdout=PIPE,
                    stderr=PIPE, shell=1).communicate()[0].split(os.linesep)[0])
                    if execs[prog]:
                        break
            else:
                try:  # Comprobación en Linux
                    Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
                except OSError:
                    SI = QMessageBox.Yes
                    NO = QMessageBox.No
                    r = QMessageBox.question(self, self.trUtf8("Advertencia!"),
                        self.trUtf8("El compilador GCC no está instalado!\n\n"
                        "Instalar?"), SI | NO)
                    if r == SI:
                        #FIXME: Revisar!!
                        instalador = recursos.INSTALADOR
                        Popen(instalador)

    def guardar_configuraciones(self):
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        archivosAbiertos_ = self.contenedor_principal.get_documentos_abiertos()
        if qconfig.value('configuraciones/general/cargarArchivos',
            True).toBool():
                qconfig.setValue('archivosAbiertos/mainTab',
                    archivosAbiertos_[0])
                qconfig.setValue('archivosAbiertos/archivosRecientes',
                    self.contenedor_principal.tab.get_archivos_recientes)