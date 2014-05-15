#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QObject

from side_c import recursos


class MenuArchivo(QObject):

    def __init__(self, menu_archivo, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide

        # Acciones
        accionNuevo = menu_archivo.addAction(QIcon(
            recursos.ICONOS['nuevo']), self.trUtf8("Nuevo"))
        accionAbrir = menu_archivo.addAction(QIcon(
            recursos.ICONOS['abrir']), self.trUtf8("Abrir"))
        accionGuardar = menu_archivo.addAction(QIcon(
            recursos.ICONOS['guardar']), self.trUtf8("Guardar"))
        accionGuardar_como = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar-como']),
            self.trUtf8("Guardar como..."))
        accionGuardar_todos = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar']), self.trUtf8("Guardar todos"))
        menu_archivo.addSeparator()
        accionImprimir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['print']), self.trUtf8("Imprimir archivo"))
        menu_archivo.addSeparator()
        accionCerrar = menu_archivo.addAction(self.trUtf8("Cerrar"))
        accionCerrar_todos = menu_archivo.addAction(
            self.trUtf8("Cerrar todos"))
        accionCerrar_excepto = menu_archivo.addAction(
            self.trUtf8("Cerrar excepto actual"))
        menu_archivo.addSeparator()
        accionSalir = menu_archivo.addAction(QIcon(recursos.ICONOS['salir']),
            self.trUtf8("Salir"))

        # Conexiones
        accionNuevo.triggered.connect(self.archivo_nuevo)
        accionSalir.triggered.connect(ide.close)

    def archivo_nuevo(self):
        pass