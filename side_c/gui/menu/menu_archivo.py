#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QObject

from side_c import recursos


class MenuArchivo(QObject):

    def __init__(self, menu_archivo, toolbar, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide

        # Acciones
        accionNuevo = menu_archivo.addAction(QIcon(
            recursos.ICONOS['nuevo']), self.trUtf8("Nuevo"))
        accionNuevo.setShortcut(Qt.CTRL + Qt.Key_N)
        accionAbrir = menu_archivo.addAction(QIcon(
            recursos.ICONOS['abrir']), self.trUtf8("Abrir"))
        accionAbrir.setShortcut(Qt.CTRL + Qt.Key_O)
        accionGuardar = menu_archivo.addAction(QIcon(
            recursos.ICONOS['guardar']), self.trUtf8("Guardar"))
        accionGuardar.setShortcut(Qt.CTRL + Qt.Key_S)
        accionGuardar_como = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar-como']),
            self.trUtf8("Guardar como..."))
        accionGuardar_todos = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar']), self.trUtf8("Guardar todos"))
        menu_archivo.addSeparator()
        accionImprimir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['print']), self.trUtf8("Imprimir archivo"))
        accionImprimir.setShortcut(Qt.CTRL + Qt.Key_P)
        menu_archivo.addSeparator()
        accionCerrar = menu_archivo.addAction(self.trUtf8("Cerrar"))
        accionCerrar.setShortcut(Qt.CTRL + Qt.Key_W)
        accionCerrar_todos = menu_archivo.addAction(
            self.trUtf8("Cerrar todos"))
        accionCerrar_excepto = menu_archivo.addAction(
            self.trUtf8("Cerrar excepto actual"))
        menu_archivo.addSeparator()
        accionSalir = menu_archivo.addAction(QIcon(recursos.ICONOS['salir']),
            self.trUtf8("Salir"))

        self.items_toolbar = {
            "nuevo-archivo": accionNuevo,
            "abrir-archivo": accionAbrir,
            "guardar-archivo": accionGuardar,
            "guardar-como-archivo": accionGuardar_como
            }

        # Conexiones
        self.connect(accionNuevo, SIGNAL("triggered()"),
            self.ide.contenedor_principal.agregar_editor)
        accionSalir.triggered.connect(ide.close)

    def archivo_nuevo(self):
        pass