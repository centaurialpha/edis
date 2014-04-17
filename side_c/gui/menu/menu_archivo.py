#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject


class MenuArchivo(QObject):

    def __init__(self, menu_archivo, ide):
        super(MenuArchivo, self).__init__()

        # Contenedor del Widget Principal
        self.ide = ide

        # Acciones
        accionNuevo = menu_archivo.addAction(self.tr("Nuevo"))
        accionAbrir = menu_archivo.addAction(self.tr("Abrir"))
        accionGuardar = menu_archivo.addAction(self.tr('Guardar'))
        accionGuardar_como = menu_archivo.addAction(self.tr('Guardar como...'))
        menu_archivo.addSeparator()
        accionSalir = menu_archivo.addAction(self.tr("Salir"))

        # Conexiones
        accionNuevo.triggered.connect(self.archivo_nuevo)
        accionSalir.triggered.connect(ide.close)

    def archivo_nuevo(self):
        pass