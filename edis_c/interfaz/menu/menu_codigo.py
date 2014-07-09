#*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

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

import os

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut
from PyQt4.QtCore import QObject

#from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from edis_c import recursos


class MenuCodigoFuente(QObject):

    def __init__(self, menu_codigo, toolbar, ide):
        super(MenuCodigoFuente, self).__init__()

        self.ide = ide

        # Cargar shortcut
        self.atajoCompilar = QShortcut(recursos.ATAJOS['compilar'], self.ide)
        self.atajoEjecutar = QShortcut(recursos.ATAJOS['ejecutar'], self.ide)
        self.atajoCompilarEjecutar = QShortcut(recursos.ATAJOS['comp-ejec'],
            self.ide)

        # Conexiones
        self.connect(self.atajoCompilar, SIGNAL("activated()"),
            self.metodo_compilar)
        self.connect(self.atajoEjecutar, SIGNAL("activated()"),
            self.metodo_ejecutar)
        self.connect(self.atajoCompilarEjecutar, SIGNAL("activated()"),
            self.metodo_compilar_ejecutar)

        # Acciones
        self.accionCompilar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['compilar']), self.trUtf8("Compilar"))
        self.cargar_status_tip(self.accionCompilar,
            self.trUtf8("Compilar archivo actual"))
        self.accionEjecutar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['ejecutar']), self.trUtf8("Ejecutar"))
        self.cargar_status_tip(self.accionEjecutar,
            self.trUtf8("Ejecutar programa"))
        self.accionCompilarEjecutar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['comp-ejec']),
            self.trUtf8("Compilar y ejecutar"))
        self.cargar_status_tip(self.accionCompilarEjecutar,
            self.trUtf8("Compilar archivo y ejecutar inmediatamente"))
        self.accionFrenar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['frenar']), self.trUtf8("Frenar programa"))
        self.cargar_status_tip(self.accionFrenar,
            self.trUtf8("Terminar programa"))

        # Acciones desactivadas
        #self.accionCompilar.setEnabled(False)
        #self.accionEjecutar.setEnabled(False)
        #self.accionCompilarEjecutar.setEnabled(False)

        self.items_toolbar = {
            "compilar-archivo": self.accionCompilar,
            "ejecutar-archivo": self.accionEjecutar,
            "compilar_ejecutar-archivo": self.accionCompilarEjecutar,
            "frenar": self.accionFrenar
            }

        # Conexión a slots
        self.connect(self.accionCompilar, SIGNAL("triggered()"),
            self.metodo_compilar)
        self.connect(self.accionEjecutar, SIGNAL("triggered()"),
            self.metodo_ejecutar)

    def cargar_status_tip(self, accion, texto):
        self.ide.cargar_status_tips(accion, texto)

    def metodo_compilar(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if not editorW:
            return None

        path_name = self.ide.contenedor_principal.guardar_archivo(editorW)
        nombre_salida = os.path.basename(path_name).split('.')[0]
        #os.popen('gcc -Wall -o %s %s' % (nombre_salida, path_name))
        #print "Compilado"

        self.ide.contenedor_secundario.compilar_archivo(
            nombre_salida, path_name)

    def metodo_ejecutar(self):
        self.ide.contenedor_secundario.ejecutar_archivo()

    def metodo_compilar_ejecutar(self):
        pass