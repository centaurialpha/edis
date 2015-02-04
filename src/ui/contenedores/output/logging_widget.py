# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import time

from PyQt4.QtGui import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QColor,
    QMenu,
    QAction
    )


class Logging(QWidget):

    def __init__(self, parent):
        super(Logging, self).__init__()
        self.parent = parent
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)

        self.logging_list = QListWidget()
        vLayout.addWidget(self.logging_list)

    def add_log(self, filename, typ):
        self.parent.item_cambiado(2)
        item = QListWidgetItem(
            self.trUtf8("%s: %s %s" % (time.strftime("%H:%M:%S"),
                        filename, typ)))
        if self.logging_list.count() % 2 == 0:
            item.setBackground(QColor('lightgray'))
        self.logging_list.addItem(item)

    def contextMenuEvent(self, evento):
        menu = QMenu(self)
        limpiar = QAction(self.tr("Limpiar"), self)
        menu.addAction(limpiar)

        limpiar.triggered.connect(self.logging_list.clear)

        menu.exec_(evento.globalPos())