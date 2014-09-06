#-*- coding: utf-8 -*-

# <Encargado de correr la Interfáz.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

# Módulos Python
import os
import sys
from re import findall
from subprocess import Popen
from subprocess import PIPE

# Módulos QtGui
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMessageBox

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings

# Módulos EDIS
import edis_c
from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.interfaz import actualizaciones
from edis_c.interfaz.menu import menu_archivo
from edis_c.interfaz.menu import menu_editar
from edis_c.interfaz.menu import menu_ver
from edis_c.interfaz.menu import menu_buscar
from edis_c.interfaz.menu import menu_herramientas
from edis_c.interfaz.menu import menu_ejecucion
from edis_c.interfaz.menu import menu_acerca_de
from edis_c.interfaz import widget_central
from edis_c.interfaz import barra_de_estado
from edis_c.interfaz.distribuidor import Distribuidor
from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.contenedor_secundario import contenedor_secundario
from edis_c.interfaz.widgets import notificacion
from edis_c.interfaz.widgets import widget_buscar
from edis_c.interfaz.widgets import line_busqueda
from edis_c.interfaz.dialogos import buscar_en_archivos


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
        self.comprobar_compilador()
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
        self.toolbar_busqueda = QToolBar(self)
        self.toolbar_busqueda.addWidget(line_busqueda.Widget())
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
        # Notificaciones
        self.noti = notificacion.Notificacion(self)
        # Barra de estado
        self.barra_de_estado = barra_de_estado.BarraDeEstado(self)
        #self.barra_de_estado.hide()
        self.setStatusBar(self.barra_de_estado)
        # Distribuidor
        self.distribuidor = Distribuidor(self)
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
        self.connect(self.contenedor_principal,
            SIGNAL("archivoGuardado(QString)"), self.mostrar_barra_de_estado)
        self.connect(self._menu_archivo, SIGNAL("abrirArchivo(QString)"),
            self.contenedor_principal.abrir_archivo)

        # Método para cargar items en las toolbar
        self.cargar_toolbar()

        if configuraciones.PAGINA_BIENVENIDA:
            self.contenedor_principal.mostrar_pagina_de_bienvenida()

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
        self.buscador = widget_buscar.WidgetBusqueda(self)
        self.buscador_archivos = buscar_en_archivos.WidgetBuscarEnArchivos(self)
        self.connect(self.contenedor_principal,
            SIGNAL("desactivarBienvenida()"),
            self.desactivar_pagina_de_bienvenida)
        self.connect(self.contenedor_principal, SIGNAL(
            "currentTabChanged(QString)"), self.cambiar_titulo_de_ventana)
        self.connect(self.contenedor_principal, SIGNAL("nuevoArchivo()"),
            self.contenedor_principal.agregar_editor)
        self.connect(self.contenedor_principal, SIGNAL("abrirArchivo()"),
            self.contenedor_principal.abrir_archivo)
        widget_central.agregar_buscador_de_archivos(self.buscador_archivos)
        widget_central.agregar_contenedor_central(self.contenedor_principal)
        widget_central.agregar_contenedor_bottom(self.contenedor_secundario)
        widget_central.agregar_buscador(self.buscador)

        self.connect(self.contenedor_principal, SIGNAL(
            "cursorPositionChange(int, int)"), self._linea_columna)

    def desactivar_pagina_de_bienvenida(self):
        """ Desactiva la página de inicio al iniciar próxima sesión. """

        configuraciones.PAGINA_BIENVENIDA = False
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        qconfig.setValue('configuraciones/general/paginaBienvenida',
            configuraciones.PAGINA_BIENVENIDA)
        self.contenedor_principal.tab_actual.cerrar_tab()

    def cargar_toolbar(self):
        #""" Carga los items en el toolbar
            #menus: lista de menus o menu.
            #toolbar: QToolBar
            #items: lista de items
        #"""
        #self.toolbar.clear()
        #items_toolbar = {}

        #if isinstance(menus, list):
            #for menu in menus:
                #items_toolbar.update(menu.items_toolbar)
        #else:
            #items_toolbar.update(menus.items_toolbar)

        #for item in items:
            #if item == 'separador':
                #toolbar.addSeparator()
            #else:
                #item_tool = items_toolbar.get(item, None)

                #if item_tool is not None:
                    #toolbar.addAction(item_tool)
        self.toolbar.clear()
        items = {}

        items.update(self._menu_archivo.items_toolbar)
        items.update(self._menu_editar.items_toolbar)
        items.update(self._menu_buscar.items_toolbar)
        items.update(self._menu_ver.items_toolbar)
        items.update(self._menu_herramientas.items_toolbar)
        items.update(self._menu_ejecucion.items_toolbar)

        for i in configuraciones.BARRA_HERRAMIENTAS_ITEMS:
            if i == 'separador':
                self.toolbar.addSeparator()
            else:
                item = items.get(i, None)
                if item is not None:
                    self.toolbar.addAction(item)

    def cargar_status_tips(self, accion, texto):
        accion.setStatusTip(texto)

    def cambiar_titulo_de_ventana(self, titulo):
        """ Cambia el título de la ventana cuando la pestaña cambia de nombre,
        esta emite la señal de cambio. """

        if titulo == edis_c.__nombre__:
            titulo = ""
            return

        nombre_con_extension = os.path.basename(str(titulo)).split('/')[0]
        self.setWindowTitle(
            #nombre_con_extension + ' (' + titulo + ')' + ' - EDIS-C')
            nombre_con_extension + ' (' + titulo + ') - ' + edis_c.__nombre__)

    def _linea_columna(self):
        """ Muestra el número de línea y columna del archivo actual. """

        editor = self.contenedor_principal.devolver_editor_actual()
        if editor is not None:
            linea = editor.textCursor().blockNumber() + 1
            columna = editor.textCursor().columnNumber()
            total_lineas = editor.devolver_cantidad_de_lineas()
            self.barra_de_estado.linea_columna.actualizar_linea_columna(
                linea, total_lineas, columna)

    def closeEvent(self, evento):
        """ Al cerrar EDIS se comprueba los archivos sin guardar """

        SI = QMessageBox.Yes
        CANCELAR = QMessageBox.Cancel

        if self.contenedor_principal.check_tabs_sin_guardar() and \
        configuraciones.CONFIRMAR_AL_CERRAR:
            archivos_sin_guardar = \
                self.contenedor_principal.devolver_archivos_sin_guardar()
            #print type(archivos_sin_guardar)
            txt = '\n'.join(archivos_sin_guardar)
            v = QMessageBox.question(self,
                self.trUtf8("Archivos sin guardar!"),
                self.trUtf8("Estos archivos no se han guardado:\n"
                "%1\n\n¿Guardar cambios?").arg(txt),
                SI, QMessageBox.No, CANCELAR)

            if v == SI:
                self.contenedor_principal.guardar_todo()

            if v == CANCELAR:
                evento.ignore()
        self.guardar_configuraciones()

    def mostrar_barra_de_estado(self, mensaje, duracion=4000):
        """ Muestra la barra de estado. """

        self.noti.set_message(mensaje, duracion)
        self.noti.show()

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