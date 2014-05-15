#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

import webbrowser

import side_c
from side_c import recursos


class AcercaDeIDE(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)

        self.setWindowTitle(self.trUtf8("Acerca de SIDE-C"))
        self.setMaximumSize(QSize(0, 0))
        vbox = QVBoxLayout(self)
        vbox.setMargin(0)

        self.tab = Tabs()
        self.tab.setMovable(False)
        self.tab.setTabsClosable(False)

        vbox.addWidget(self.tab)
        self.setLayout(vbox)


class Tabs(QTabWidget):

    def __init__(self):
        super(Tabs, self).__init__()

        self.acerca_de_side = AcercaDeSide()
        self.acerca_de_creadores = AcercaDeCreadores()

        self.addTab(self.acerca_de_side, self.trUtf8("Acerca de SIDE-C"))
        self.addTab(self.acerca_de_creadores, self.trUtf8("Creadores"))


class AcercaDeSide(QWidget):

    def __init__(self):
        super(AcercaDeSide, self).__init__()

        layout_vertical = QVBoxLayout(self)

        titulo_label = QLabel(
            '<h1>SIDE-C</h1>')
        titulo_label.setAlignment(Qt.AlignCenter)
        layout_vertical.addWidget(titulo_label)
        logo = QPixmap(recursos.ICONOS['icono'])
        self.logo_label = QLabel()
        self.logo_label.setPixmap(logo)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout_vertical.addWidget(self.logo_label)
        comentario_label = QLabel(
            '<i>Entorno de Desarrollo Integrado Simple</i>\n')
        comentario_label.setAlignment(Qt.AlignCenter)
        layout_vertical.addWidget(comentario_label)
        self.setLayout(layout_vertical)

        descripcion_label = QLabel(
            self.trUtf8("""<b>SIDE-C</b> es un IDE para el lenguaje de
programacion C, simple y ligero.\n"""))
        descripcion_label.setAlignment(Qt.AlignLeft)

        layout_vertical.addWidget(descripcion_label)

        version_side = QLabel(
            ('Version: %s') % (side_c.__version__))
        layout_vertical.addWidget(version_side)

        link_codigo_fuente = QLabel(
            ('Codigo fuente: <a href="%s">%s</a>') %
            (side_c.__codigo_fuente__, side_c.__codigo_fuente__))
        layout_vertical.addWidget(link_codigo_fuente)

        self.connect(link_codigo_fuente, SIGNAL("linkActivated(QString)"),
            self.activar_link)

    def activar_link(self, link):
        webbrowser.open(str(link))


class AcercaDeCreadores(QWidget):

    def __init__(self):
        super(AcercaDeCreadores, self).__init__()

        vbox = QVBoxLayout(self)
        label_g = QLabel(
            """Gabriel Acosta <acostadariogabriel@gmail.com> """)
        label_m = QLabel(
            "Martin Miranda <debianitram@gmail.com>")

        label_g.setAlignment(Qt.AlignCenter)
        label_m.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label_g)
        vbox.addWidget(label_m)

        self.setLayout(vbox)