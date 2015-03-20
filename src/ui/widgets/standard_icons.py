# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QApplication

# Módulos EDIS
from creador_widget import get_icono_estandard


class MostrarIconos(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        layout = QHBoxLayout()
        row_nb = 14
        cindex = 0
        for child in dir(QStyle):
            if child.startswith('SP_'):
                if cindex == 0:
                    col_layout = QVBoxLayout()
                icono_layout = QHBoxLayout()
                icono = get_icono_estandard(child)
                label = QLabel()
                label.setPixmap(icono.pixmap(32, 32))
                icono_layout.addWidget(label)
                lineEdit = QLineEdit(child.replace('SP_', ''))
                lineEdit.setReadOnly(True)
                icono_layout.addWidget(lineEdit)
                col_layout.addLayout(icono_layout)
                cindex = (cindex + 1) % row_nb
                if cindex == 0:
                    layout.addLayout(col_layout)
        self.setLayout(layout)
        self.setWindowTitle('Iconos Estandard')
        self.setWindowIcon(get_icono_estandard('TitleBarMenuButton'))


def mostrar_iconos_estandard():
    app = QApplication([])
    dialogo = MostrarIconos()
    dialogo.show()
    import sys
    sys.exit(app.exec_())


if __name__ == "__main__":
    mostrar_iconos_estandard()
