#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c import recursos


class MenuCodigoFuente(QObject):

    def __init__(self, menu_codigo, toolbar, ide):
        super(MenuCodigoFuente, self).__init__()

        self.ide = ide
        # Cargar shortcut

        # Conexiones

        # Acciones
        accionCompilar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['compilar']), self.trUtf8("Compilar"))
        accionCompilar.setShortcut(Qt.CTRL + Qt.Key_F5)
        accionEjecutar = menu_codigo.addAction(
            QIcon(recursos.ICONOS['ejecutar']), self.trUtf8("Ejecutar"))
        accionEjecutar.setShortcut(Qt.CTRL + Qt.Key_F6)
        accionCompilar_Ejecutar = menu_codigo.addAction(
            self.trUtf8("Compilar y ejecutar"))

        self.items_toolbar = {
            "compilar-archivo": accionCompilar,
            "ejecutar-archivo": accionEjecutar,
            "ejecutar_compilar-archivo": accionCompilar_Ejecutar
            }

        # Conexión a slots
        self.connect(accionCompilar, SIGNAL("triggered()"),
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




