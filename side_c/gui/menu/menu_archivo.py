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
            recursos.ICONOS['nuevo']), self.tr("Nuevo"))
        accionAbrir = menu_archivo.addAction(QIcon(
            recursos.ICONOS['abrir']), self.tr("Abrir"))
        accionGuardar = menu_archivo.addAction(QIcon(
            recursos.ICONOS['guardar']), self.tr('Guardar'))
        accionGuardar_como = menu_archivo.addAction(
            QIcon(recursos.ICONOS['guardar-como']), self.tr('Guardar como...'))
        menu_archivo.addSeparator()
        accionImprimir = menu_archivo.addAction(
            QIcon(recursos.ICONOS['print']), self.tr('Imprimir archivo'))
        menu_archivo.addSeparator()
        accionSalir = menu_archivo.addAction(QIcon(recursos.ICONOS['salir']),
            self.tr("Salir"))

        # Conexiones
        accionNuevo.triggered.connect(self.archivo_nuevo)
        accionSalir.triggered.connect(ide.close)

    def archivo_nuevo(self):
        pass