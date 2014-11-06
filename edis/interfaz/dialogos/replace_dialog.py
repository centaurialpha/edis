# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.


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