#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c import recursos


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
        self.accionEjecutar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['ejecutar']), self.trUtf8("Ejecutar"))
        self.accionCompilarEjecutar = menu_codigo.addAction(
            self.trUtf8("Compilar y ejecutar"))

        self.items_toolbar = {
            "compilar-archivo": self.accionCompilar,
            "ejecutar-archivo": self.accionEjecutar,
            "ejecutar_compilar-archivo": self.accionCompilarEjecutar
            }

        # Conexión a slots
        self.connect(self.accionCompilar, SIGNAL("triggered()"),
            self.metodo_compilar)

    def metodo_compilar(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        path_name = self.ide.contenedor_principal.guardar_archivo(editorW)
        import os
        nombre_salida = os.path.basename(path_name).split('.')[0]
        #os.popen('gcc -Wall -o %s %s' % (nombre_salida, path_name))
        #print "Compilado"

        self.ide.contenedor_secundario.compilar_archivo(
            nombre_salida, path_name)

    def metodo_ejecutar(self):
        pass

    def metodo_compilar_ejecutar(self):
        pass