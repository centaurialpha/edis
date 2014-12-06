# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QFileSystemModel,
    )

from PyQt4.QtCore import (
    SIGNAL,
    QModelIndex,
    pyqtSlot,
    #QStringList,
    QDir
    )


class Explorador(QWidget):
    """ Explorador de archivos basado en QFileSystemModel """

    def __init__(self, parent=None):
        super(Explorador, self).__init__()
        self.setStyleSheet("background: #616266; color: #bfbfbf")
        vb = QVBoxLayout(self)
        vb.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeView()
        self.tree.header().setHidden(True)
        self.tree.setAnimated(True)

        self.model = QFileSystemModel(self.tree)
        home_path = QDir.toNativeSeparators(QDir.homePath())
        self.model.setRootPath(home_path)
        #filtro = QStringList("")
        #filtro << "*.c" << "*.h"  # Filtro
        self.tree.setModel(self.model)
        self.tree.setRootIndex(QModelIndex(self.model.index(home_path)))
        #self.model.setNameFilters(filtro)
        self.model.setNameFilterDisables(False)

        # Se ocultan algunas columnas (size, type, y date modified)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        vb.addWidget(self.tree)

        # Conexión a slot
        self.tree.doubleClicked.connect(self.doble_click)

    @pyqtSlot(QModelIndex)
    def doble_click(self, i):
        ind = self.model.index(i.row(), 0, i.parent())
        archivo = self.model.filePath(ind)
        # Señal emitida -> ruta completa del archivo
        self.emit(SIGNAL("dobleClickArchivo(QString)"), archivo)