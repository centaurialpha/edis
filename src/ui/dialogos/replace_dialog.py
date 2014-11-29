# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QApplication
    )


class ReplaceDialog(QDialog):

    def __init__(self):
        super(ReplaceDialog, self).__init__()
        self.setWindowTitle(self.trUtf8("Reemplazar"))
        boxv = QVBoxLayout(self)
        boxh = QHBoxLayout()
        boxhh = QHBoxLayout()

        lbl_search = QLabel(self.trUtf8("Buscar por:"))
        boxh.addWidget(lbl_search)

        self.line_search = QLineEdit()
        boxh.addWidget(self.line_search)
        boxv.addLayout(boxh)

        lbl_replace = QLabel(self.trUtf8("Reemplazar por:"))
        boxhh.addWidget(lbl_replace)

        self.line_replace = QLineEdit()
        boxhh.addWidget(self.line_replace)
        boxv.addLayout(boxhh)


app = QApplication([])
import sys
w = ReplaceDialog()
w.show()
sys.exit(app.exec_())