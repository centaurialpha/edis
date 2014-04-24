#-*- coding: ISO-8859-15 -*-
#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

import webbrowser

import side_c
from side_c import recursos


class AcercaDeIDE(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.tr("Acerca de SIDE-C"))
        self.setMaximumSize(QSize(0, 0))

        # Layout Vertical
        lay_vertical = QVBoxLayout(self)
        # Layout Horizontal
        lay_horizontal = QHBoxLayout()

        logo = QPixmap(recursos.ICONOS['icono'])
        self.logo_label = QLabel()
        self.logo_label.setPixmap(logo)
        lay_horizontal.addWidget(self.logo_label)

        titulo_label = QLabel(
            '<h1>SIDE-C</h1>\n<i>Entorno de Desarrollo Integrado Simple</i>')
        titulo_label.setAlignment(Qt.AlignCenter)
        lay_horizontal.addWidget(titulo_label)
        lay_vertical.addLayout(lay_horizontal)

        # Descripcion
        descripcion_label = QLabel(
            self.tr("""SIDE-C es un IDE para el lenguaje de programaci?n C,
simple y ligero."""))
        descripcion_label.setAlignment(Qt.AlignLeft)

        lay_vertical.addWidget(descripcion_label)

        link_codigo_fuente = QLabel(
            ('Codigo fuente: <a href="%s">%s</a>') %
            (side_c.__codigo_fuente__, side_c.__codigo_fuente__))
        lay_vertical.addWidget(link_codigo_fuente)

        self.connect(link_codigo_fuente, SIGNAL("linkActivated(QString)"),
            self.activar_link)

    def activar_link(self, link):
        webbrowser.open(str(link))