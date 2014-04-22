#-*- coding: ISO-8859-15 -*-
#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt


class AcercaDeIDE(QDialog):

    def __init__(self):
        super(AcercaDeIDE, self).__init__()
        self.setWindowTitle(self.tr("Acerca de SIDE-C"))
        self.setMaximumSize(QSize(0, 0))

        # Layout Vertical
        lay_vertical = QVBoxLayout(self)
        # Layout Horizontal
        lay_horizontal = QHBoxLayout()

        titulo_label = QLabel(
            '<h1>SIDE-C</h1>\n<i>Entorno de Desarrollo Integrado Simple</i>')
        titulo_label.setAlignment(Qt.AlignCenter)
        lay_horizontal.addWidget(titulo_label)
        lay_vertical.addLayout(lay_horizontal)

        # Descripción
        descripcion_label = QLabel(
            self.tr("""SIDE-C es un IDE para el lenguaje de programación C,
simple y ligero."""))
        descripcion_label.setAlignment(Qt.AlignLeft)

        lay_vertical.addWidget(descripcion_label)