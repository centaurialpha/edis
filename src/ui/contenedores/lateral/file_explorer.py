# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QTreeView,
    QFileSystemModel,
    )

from PyQt4.QtCore import (
    QModelIndex,
    pyqtSignal,
    QDir
    )


class Explorador(QTreeView):

    abriendoArchivo = pyqtSignal(['QString'])

    def __init__(self, parent=None):
        super(Explorador, self).__init__()
        # Configuración
        self.header().setHidden(True)
        self.setAnimated(True)

        # Modelo
        self.modelo = QFileSystemModel(self)
        path = QDir.toNativeSeparators(QDir.homePath())
        self.modelo.setRootPath(path)
        self.setModel(self.modelo)
        self.modelo.setNameFilters(["*.c", "*.h", "*.s"])
        self.setRootIndex(QModelIndex(self.modelo.index(path)))
        self.modelo.setNameFilterDisables(False)

        # Se ocultan algunas columnas
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        # Conexion
        self.doubleClicked.connect(self._abrir_archivo)

    def _abrir_archivo(self, i):
        if not self.modelo.isDir(i):
            indice = self.modelo.index(i.row(), 0, i.parent())
            archivo = self.modelo.filePath(indice)
            self.abriendoArchivo.emit(archivo)