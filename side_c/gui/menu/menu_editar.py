#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

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
        accionBorrar = menu_editar.addAction(
            self.trUtf8("Borrar"))
        accionSeleccionar = menu_editar.addAction(
            self.trUtf8("Seleccionar todo"))
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
            }

        # Conexiones
        self.connect(accionDeshacer, SIGNAL("triggered()"),
            self.ide.contenedor_principal.deshacer)
        self.connect(accionRehacer, SIGNAL("triggered()"),
            self.ide.contenedor_principal.rehacer)
        self.connect(accionCortar, SIGNAL("triggered()"),
            self.ide.contenedor_principal.cortar)
        self.connect(accionCopiar, SIGNAL("triggered()"),
            self.ide.contenedor_principal.copiar)
        self.connect(accionPegar, SIGNAL("triggered()"),
            self.ide.contenedor_principal.pegar)
        self.connect(accionBorrar, SIGNAL("triggered()"),
            self.ide.contenedor_principal.borrar)
        self.connect(accionSeleccionar, SIGNAL("triggered()"),
            self.ide.contenedor_principal.seleccionar_todo)

    def _configuraciones(self):
        self.preferencias = preferencias.Configuraciones(self.ide)
        self.preferencias.show()
