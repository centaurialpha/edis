#-*- coding: utf-8 -*-

from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

from edis_c.interfaz import widget_buscar
from edis_c import recursos


class MenuBuscar(QObject):

    def __init__(self, menu_buscar, ide):
        super(MenuBuscar, self).__init__()

        self.ide = ide

        # Shortcut
        self.atajoBuscar = QShortcut(recursos.ATAJOS['buscar'], self.ide)

        # Conexión
        self.connect(self.atajoBuscar, SIGNAL("activated()"),
            widget_buscar.WidgetBuscar().show)

        accionBuscar = menu_buscar.addAction(self.trUtf8("Buscar"))

        self.connect(accionBuscar, SIGNAL("triggered()"),
            widget_buscar.WidgetBuscar().show)