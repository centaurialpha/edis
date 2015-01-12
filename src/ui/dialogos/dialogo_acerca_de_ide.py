# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import webbrowser

# Módulos QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTextBrowser

# Módulos QtCore
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QString

# Módulos EDIS
from src import ui
from src import recursos
from src.helpers import configuraciones


class AcercaDeIDE(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)

        self.setWindowTitle(self.trUtf8("Acerca de EDIS"))
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
        self.licencia = Licencia()

        self.addTab(self.acerca_de_side, self.trUtf8("Acerca de EDIS"))
        self.addTab(self.acerca_de_creadores, self.trUtf8("Creadores"))
        self.addTab(self.licencia, self.trUtf8("Licencia"))


class AcercaDeSide(QWidget):

    def __init__(self):
        super(AcercaDeSide, self).__init__()

        layout_vertical = QVBoxLayout(self)

        titulo_label = QLabel(
            self.trUtf8('<h1>EDIS</h1><i>Seiryü</i>'))
        titulo_label.setAlignment(Qt.AlignCenter)
        if configuraciones.LINUX:
            so_label = QLabel(
                self.trUtf8("<h5><i>(En GNU/Linux)</i></h5>"))
        else:
            so_label = QLabel(
                self.trUtf8("<h5><i>(En Windows</i>)</h5>"))
        layout_vertical.addWidget(titulo_label)
        logo = QPixmap(recursos.ICONOS['icono'])
        self.logo_label = QLabel()
        self.logo_label.setPixmap(logo)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout_vertical.addWidget(self.logo_label)
        layout_vertical.addWidget(so_label)
        so_label.setAlignment(Qt.AlignCenter)
        comentario_label = QLabel(
            '<i><b>E</b>ntorno de <b>D</b>esarrollo <b>I</b>ntegrado '
            '<b>S</b>imple</i>\n')
        comentario_label.setAlignment(Qt.AlignCenter)
        layout_vertical.addWidget(comentario_label)
        self.setLayout(layout_vertical)

        descripcion_label = QLabel(
            self.trUtf8('<b>EDIS</b> es un IDE para el lenguaje de '
'programación C, simple y ligero,<br>desarrollado completamente en '
'Python y Qt (PyQt)<br>'))
        links_label = QLabel(
            ('<b>Python: </b><a href="%s"><span style="color: #4dbee8;">%s'
            '</span></a><br><b>Qt:</b> <a href="%s"><span style="color: '
            '#4dbee8;">%s</span></a><br><b>PyQt:</b> <a href="%s"><span style='
            '"color: #4dbee8;">%s</span></a>') %
        (ui.__python__, ui.__python__, ui.__qt__,
            ui.__qt__, ui.__pyqt__, ui.__pyqt__))

        descripcion_label.setAlignment(Qt.AlignLeft)

        layout_vertical.addWidget(descripcion_label)
        layout_vertical.addWidget(links_label)

        version_edis = QLabel(
            ('<b>Version: </b> %s') % (ui.__version__))
        layout_vertical.addWidget(version_edis)

        link_codigo_fuente = QLabel(
            ('<b>Codigo fuente: </b> <a href="%s"><span style=" '
            'color: #4dbee8;">%s</span></a>') %
            (ui.__codigo_fuente__, ui.__codigo_fuente__))
        layout_vertical.addWidget(link_codigo_fuente)

        # Conexiones
        link_codigo_fuente.linkActivated[QString].connect(self.activar_link)
        links_label.linkActivated[QString].connect(self.activar_link)

    def activar_link(self, link):
        webbrowser.open(str(link))


class AcercaDeCreadores(QWidget):

    def __init__(self):
        super(AcercaDeCreadores, self).__init__()

        vbox = QVBoxLayout(self)
        label = QLabel(self.trUtf8(
'<b>Gabriel Acosta</b><br><i>acostadariogabriel@gmail.com</i><br>'
'<b>Martín Miranda</b><br><i>debianitram@gmail.com</i>'))

        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

        self.setLayout(vbox)


class Licencia(QWidget):

    def __init__(self):
        super(Licencia, self).__init__()

        self.setWindowTitle("Licencia")
        vbox = QVBoxLayout(self)

        self.contenedor = QTextBrowser()
        vbox.addWidget(self.contenedor)

        self.leer_licencia()

    def leer_licencia(self):
        try:
            with open(recursos.LICENCIA, 'r') as l:
                data = l.read()
                self.contenedor.setText(data)
        except:
            self.contenedor.setText("Archivo no encontrado")
