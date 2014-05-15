#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject


class MenuEditar(QObject):
    """ Items del menu Editar """

    def __init__(self, menu_editar, ide):
        super(MenuEditar, self).__init__()

        # Agrega acciones
        accionDeshacer = menu_editar.addAction(self.trUtf8("Deshacer"))
        accionRehacer = menu_editar.addAction(self.trUtf8("Rehacer"))
        accionCortar = menu_editar.addAction(self.trUtf8("Cortar"))
        accionCopiar = menu_editar.addAction(self.trUtf8("Copiar"))
        accionPegar = menu_editar.addAction(self.trUtf8("Pegar"))
        menu_editar.addSeparator()
        accionBuscar = menu_editar.addAction(self.trUtf8("Buscar"))

        # Conexiones
        accionDeshacer.triggered.connect(self._funcion_deshacer)
        accionRehacer.triggered.connect(self._funcion_rehacer)
        accionCortar.triggered.connect(self._funcion_cortar)
        accionCopiar.triggered.connect(self._funcion_copiar)
        accionPegar.triggered.connect(self._funcion_pegar)
        accionBuscar.triggered.connect(self._funcion_pegar)

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