# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QListWidget,
    QVBoxLayout,
    QLabel
    )


class DialogoDependencias(QDialog):

    def __init__(self, dependencias, parent=None):
        super(DialogoDependencias, self).__init__(parent)
        self.setWindowTitle(self.tr("Dependencias"))
        box = QVBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        box.addWidget(QLabel(self.tr("Las siguientes dependencias no se\n"
                            "han encontrado en el sistema:")))
        self.lista_dependencias = QListWidget()
        box.addWidget(self.lista_dependencias)
        self.lista_dependencias.addItems([clave for clave, valor in
                                    list(dependencias.items()) if not valor])