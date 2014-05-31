#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

from side_c.gui.editor import acciones_
from side_c import recursos


class MenuArchivo(QObject):
    """ Items del menú Archivo """

    def __init__(self, menu_archivo, toolbar, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide

        # Se cargan los shortcut
        self.atajoNuevo = QShortcut(recursos.ATAJOS['nuevo'], self.ide)
        self.atajoAbrir = QShortcut(recursos.ATAJOS['abrir'], self.ide)
        self.atajoGuardar = QShortcut(recursos.ATAJOS['guardar'], self.ide)
        self.atajoCerrarTab = QShortcut(recursos.ATAJOS['cerrar-tab'], self.ide)

        # Conexiones
        self.connect(self.atajoNuevo, SIGNAL("activated()"),
            self.ide.contenedor_principal.agregar_editor)
        self.connect(self.atajoAbrir, SIGNAL("activated()"),
            self.ide.contenedor_principal.abrir_archivo)
        self.connect(self.atajoGuardar, SIGNAL("activated()"),
            self.ide.contenedor_principal.guardar_archivo)
        self.connect(self.atajoCerrarTab, SIGNAL("activated()"),
            self.ide.contenedor_principal.cerrar_tab)

        # Acciones
        self.accionNuevo = menu_archivo.addAction(
            QIcon(recursos.ICONOS['nuevo']), self.trUtf8("Nuevo archivo"))
        self.accionNuevo.setShortcut(recursos.ATAJOS['nuevo'])
        self.accionAbrir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['abrir']), self.trUtf8("Abrir archivo"))
        self.accionAbrir.setShortcut(recursos.ATAJOS['abrir'])
        self.accionGuardar = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar']), self.trUtf8("Guardar"))
        self.accionGuardar.setShortcut(recursos.ATAJOS['guardar'])
        self.accionGuardarComo = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar-como']), self.trUtf8("Guardar como"))
        menu_archivo.addSeparator()
        self.accionImprimir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['print']), self.trUtf8("Imprimir archivo"))
        self.accionImprimir.setShortcut(recursos.ATAJOS['imprimir'])
        menu_archivo.addSeparator()
        self.accionCerrarTab = menu_archivo.addAction(
            self.trUtf8("Cerrar"))
        self.accionCerrarTab.setShortcut(recursos.ATAJOS['cerrar-tab'])
        self.accionCerrarTodo = menu_archivo.addAction(
            self.trUtf8("Cerrar todo"))
        self.accionCerrarExceptoActual = menu_archivo.addAction(
            self.trUtf8("Cerrar excepto actual"))
        menu_archivo.addSeparator()
        self.accionSalir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['salir']), self.trUtf8("Salir"))

        # Conexión a métodos
        self.accionNuevo.triggered.connect(
            self.ide.contenedor_principal.agregar_editor)
        self.accionAbrir.triggered.connect(
            self.ide.contenedor_principal.abrir_archivo)
        self.accionGuardar.triggered.connect(
            self.ide.contenedor_principal.guardar_archivo)
        self.accionImprimir.triggered.connect(
            self.imprimir_)
        self.accionCerrarTab.triggered.connect(
            self.ide.contenedor_principal.cerrar_tab)
        self.accionCerrarExceptoActual.triggered.connect(
            self.ide.contenedor_principal.cerrar_excepto_actual)
        self.accionCerrarTodo.triggered.connect(
            self.ide.contenedor_principal.cerrar_todo)

        # Toolbar
        self.items_toolbar = {
            "nuevo-archivo": self.accionNuevo,
            "abrir-archivo": self.accionAbrir,
            "guardar-archivo": self.accionGuardar,
            "guardar-como-archivo": self.accionGuardarComo
            }

    def imprimir_(self):
        """ Llama al método para imprimir archivo actual """

        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW is not None:
            nombre = "Documento_nuevo.pdf"

            acciones_.imprimir_archivo(nombre, editorW.print_)