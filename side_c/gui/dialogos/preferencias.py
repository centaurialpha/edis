#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QSize

from side_c import recursos


class Configuraciones(QDialog):

    def __init__(self, parent=None):
        super(Configuraciones, self).__init__()

        self.setWindowTitle(self.trUtf8("Configuración"))
        self.setMaximumSize(QSize(0, 0))

        vbox = QVBoxLayout(self)

        self.tabs = Tabs()
        self.tabs.setMovable(False)
        self.tabs.setTabsClosable(False)

        vbox.setMargin(0)
        vbox.addWidget(self.tabs)


class Tabs(QTabWidget):

    def __init__(self):
        super(Tabs, self).__init__()

        self.configuraciones_generales = General()
        self.cambiar_tema = CambiarTema()

        self.addTab(self.configuraciones_generales, self.trUtf8("General"))
        self.addTab(self.cambiar_tema, self.trUtf8("Tema"))


class General(QWidget):

    def __init__(self):
        super(General, self).__init__()

        #vbox = QVBoxLayout(self)


class CambiarTema(QWidget):

    def __init__(self):
        super(CambiarTema, self).__init__()
        self.setWindowTitle(self.trUtf8("Cambiar tema"))
        self.tema_por_defecto = 0
        self.tema_black_side = 1

        vbox = QVBoxLayout(self)

        label = QLabel("Elige un tema:")

        self.lista_temas = QListWidget()
        self.lista_temas.addItem("Default")
        self.lista_temas.addItem("Black SIDE")

        boton_cambiar = QPushButton(self.trUtf8("Cambiar"))

        hbox = QHBoxLayout()
        hbox.addWidget(boton_cambiar)
        hbox.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Expanding,
            QSizePolicy.Fixed))

        vbox.addWidget(label)
        vbox.addWidget(self.lista_temas)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        boton_cambiar.clicked.connect(self._cambiar_tema)

    def _cambiar_tema(self):
        if self.lista_temas.currentRow() == self.tema_por_defecto:
            tema = recursos.TEMA_POR_DEFECTO
        elif self.lista_temas.currentRow() == self.tema_black_side:

            tema = recursos.TEMA_SIDE

        fname = open(tema, 'r')
        data = fname.read()
        QApplication.instance().setStyleSheet(data)
        fname.close()
