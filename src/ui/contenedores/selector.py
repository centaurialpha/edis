# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    )

from PyQt4.QtCore import (
    #pyqtSignal,
    QUrl,
    SIGNAL,
    Qt
    )

from PyQt4.QtDeclarative import QDeclarativeView

from src import recursos
from src.ui.edis_main import EDIS


class Selector(QDialog):

    def __init__(self, parent=None):
        super(Selector, self).__init__(parent,
                Qt.Dialog | Qt.FramelessWindowHint)
        # Configuración
        self.setModal(True)
        self.setStyleSheet("background:transparent;")

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 1, 1)
        box.setSpacing(0)
        # Interfáz QML
        view = QDeclarativeView()
        view.setSource(QUrl(self.__get_qml()))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        box.addWidget(view)

        self.root = view.rootObject()
        self.__cargar()

        self.connect(self.root, SIGNAL("abrirArchivo(int)"),
                    self.__abrir_archivo)

    @staticmethod
    def __get_qml():
        return recursos.SELECTOR_QML

    def __abrir_archivo(self, indice):
        principal = EDIS.componente("principal")
        principal.cambiar_widget(indice)
        self.hide()

    def __current_indice(self):
        principal = EDIS.componente("principal")
        indice = principal.indice_actual()
        #FIXME: Mandar la señal
        #self.emit(SIGNAL("currentIndice(int)"), indice)
        self.root.item_actual(indice)

    def __cargar(self):
        principal = EDIS.componente("principal")
        archivos_abiertos_ = principal.archivos_abiertos()
        for archivo in archivos_abiertos_:
            #FIXME: modificar para güindous
            archivo = archivo.split('/')[-1]
            self.root.cargar_archivo(archivo)
        self.__current_indice()