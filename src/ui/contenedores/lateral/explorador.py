# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QTreeView,
    QFileSystemModel,
    QDockWidget
    )

from PyQt4.QtCore import (
    QModelIndex,
    pyqtSignal,
    QDir
    )


class Explorador(QDockWidget):

    abriendoArchivo = pyqtSignal(['QString'])

    def __init__(self, parent=None):
        super(Explorador, self).__init__()
        self.setWindowTitle("Explorador")
        self.explorador = QTreeView()
        self.setWidget(self.explorador)
        self.explorador.header().setHidden(True)
        self.explorador.setAnimated(True)

        # Modelo
        self.modelo = QFileSystemModel(self.explorador)
        path = QDir.toNativeSeparators(QDir.homePath())
        self.modelo.setRootPath(path)
        self.explorador.setModel(self.modelo)
        self.modelo.setNameFilters(["*.c", "*.h", "*.s"])
        self.explorador.setRootIndex(QModelIndex(self.modelo.index(path)))
        self.modelo.setNameFilterDisables(False)

        # Se ocultan algunas columnas
        self.explorador.hideColumn(1)
        self.explorador.hideColumn(2)
        self.explorador.hideColumn(3)

        # Conexion
        self.explorador.doubleClicked.connect(self._abrir_archivo)

    def _abrir_archivo(self, i):
        if not self.modelo.isDir(i):
            indice = self.modelo.index(i.row(), 0, i.parent())
            archivo = self.modelo.filePath(indice)
            self.abriendoArchivo.emit(archivo)