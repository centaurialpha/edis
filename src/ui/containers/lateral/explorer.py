# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QTreeView,
    QFileSystemModel
    )

from PyQt4.QtCore import (
    QModelIndex,
    QDir
    )

from src.ui.main import Edis


class Explorer(QTreeView):

    def __init__(self, parent=None):
        QTreeView.__init__(self)
        self.header().setHidden(True)
        self.setAnimated(True)

        # Modelo
        self.model = QFileSystemModel(self)
        path = QDir.toNativeSeparators(QDir.homePath())
        self.model.setRootPath(path)
        self.setModel(self.model)
        self.model.setNameFilters(["*.c", "*.h", "*.s"])
        self.setRootIndex(QModelIndex(self.model.index(path)))
        self.model.setNameFilterDisables(False)

        # Se ocultan algunas columnas
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        # Conexion
        self.doubleClicked.connect(self._open_file)

        Edis.load_lateral("explorer", self)

    def _open_file(self, i):
        if not self.model.isDir(i):
            indice = self.model.index(i.row(), 0, i.parent())
            archivo = self.model.filePath(indice)
            principal = Edis.get_component("principal")
            principal.open_file(archivo)


explorer = Explorer()
