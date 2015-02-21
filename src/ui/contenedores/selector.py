# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    )

from PyQt4.QtCore import (
    QUrl,
    SIGNAL,
    Qt,
    QDir
    )

from PyQt4.QtDeclarative import QDeclarativeView

from src import paths
from src.ui.main import EDIS


class Selector(QDialog):

    def __init__(self, parent=None):
        super(Selector, self).__init__(parent,
                                       Qt.Dialog | Qt.FramelessWindowHint)
        # Configuración
        self.setModal(True)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 1, 1)
        box.setSpacing(0)
        # Interfáz QML
        view = QDeclarativeView()
        qml = os.path.join(paths.PATH, "ui", "selector", "selector.qml")
        path = QDir.fromNativeSeparators(qml)
        view.setSource(QUrl.fromLocalFile(path))

        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        box.addWidget(view)

        self.root = view.rootObject()
        self.__cargar()

        self.connect(self.root, SIGNAL("abrirArchivo(int)"),
                     self.__abrir_archivo)

    def __abrir_archivo(self, indice):
        principal = EDIS.componente("principal")
        principal.cambiar_widget(indice)
        self.hide()

    def __current_indice(self):
        principal = EDIS.componente("principal")
        indice = principal.indice_actual()
        self.root.item_actual(indice)

    def __cargar(self):
        principal = EDIS.componente("principal")
        archivos_abiertos_ = principal.archivos_abiertos()
        for archivo in archivos_abiertos_:
            archivo = archivo.split('/')[-1]
            self.root.cargar_archivo(archivo)
        self.__current_indice()