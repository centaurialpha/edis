#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt

from side_c import recursos

from side_c.gui.dialogos import preferencias


class MenuEditar(QObject):
    """ Items del menú Editar """

    def __init__(self, menu_editar, toolbar, ide):
        super(MenuEditar, self).__init__()

        self.ide = ide

        # Agrega acciones
        accionDeshacer = menu_editar.addAction(
            QIcon(recursos.ICONOS['deshacer']), self.trUtf8("Deshacer"))
        accionDeshacer.setShortcut(Qt.CTRL + Qt.Key_Z)
        accionRehacer = menu_editar.addAction(
            QIcon(recursos.ICONOS['rehacer']), self.trUtf8("Rehacer"))
        accionRehacer.setShortcut(Qt.CTRL + Qt.Key_Y)
        menu_editar.addSeparator()
        accionCortar = menu_editar.addAction(
            QIcon(recursos.ICONOS['cortar']), self.trUtf8("Cortar"))
        accionCortar.setShortcut(Qt.CTRL + Qt.Key_X)
        accionCopiar = menu_editar.addAction(
            QIcon(recursos.ICONOS['copiar']), self.trUtf8("Copiar"))
        accionCopiar.setShortcut(Qt.CTRL + Qt.Key_C)
        accionPegar = menu_editar.addAction(
            QIcon(recursos.ICONOS['pegar']), self.trUtf8("Pegar"))
        accionPegar.setShortcut(Qt.CTRL + Qt.Key_V)
        menu_editar.addSeparator()
        accionBuscar = menu_editar.addAction(
            QIcon(recursos.ICONOS['buscar']), self.trUtf8("Buscar"))
        accionBuscar.setShortcut(Qt.CTRL + Qt.Key_F)
        menu_editar.addSeparator()
        accionConfiguracion = menu_editar.addAction(
            self.trUtf8("Configuración"))

        # Toolbar - Items
        self.items_toolbar = {
            "deshacer": accionDeshacer,
            "rehacer": accionRehacer,
            "cortar": accionCortar,
            "copiar": accionCopiar,
            "pegar": accionPegar,
            "buscar": accionBuscar
            }

        # Conexiones
        accionDeshacer.triggered.connect(self._funcion_deshacer)
        accionRehacer.triggered.connect(self._funcion_rehacer)
        accionCortar.triggered.connect(self._funcion_cortar)
        accionCopiar.triggered.connect(self._funcion_copiar)
        accionPegar.triggered.connect(self._funcion_pegar)
        accionBuscar.triggered.connect(self._funcion_pegar)
        accionConfiguracion.triggered.connect(self._configuraciones)

    # Métodos
    def _funcion_deshacer(self):
        pass

    def _funcion_rehacer(self):
        pass

    def _funcion_cortar(self):
        pass

    def _funcion_copiar(self):
        pass

    def _funcion_pegar(self):
        pass

    def _funcion_buscar(self):
        pass

    def _configuraciones(self):
        self.preferencias = preferencias.Configuraciones()
        self.preferencias.show()
