#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTextEdit
#from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QStyle
#from PyQt4.QtGui import QSizePolicy

from PyQt4.QtCore import SIGNAL

from edis_c.interfaz.contenedor_secundario import salida_widget
from edis_c import recursos


_instanciaContenedorSecundario = None


def ContenedorBottom(*args, **kw):
    global _instanciaContenedorSecundario
    if _instanciaContenedorSecundario is None:
        _instanciaContenedorSecundario = _ContenedorBottom(*args, **kw)

    return _instanciaContenedorSecundario


class _ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layoutV = QVBoxLayout()

        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        self.stack = Stacked()
        hbox.addWidget(self.stack)

        self.salida_ = salida_widget.EjecutarWidget()
        self.stack.addWidget(self.salida_)

        self.notas = Notas(self)
        self.stack.addWidget(self.notas)

        self.botonSalida = QPushButton(QIcon(recursos.ICONOS['terminal']), '')
        self.botonNotas = QPushButton(QIcon(recursos.ICONOS['notas']), '')
        boton_cerrar = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogCloseButton), '')

        layoutV.addWidget(self.botonSalida)
        layoutV.addWidget(self.botonNotas)
        #layoutV.addSpacerItem(QSpacerItem(0, 0, 0))
        layoutV.addWidget(boton_cerrar)
        hbox.addLayout(layoutV)

        self.connect(self.botonSalida, SIGNAL("clicked()"),
            lambda: self.item_cambiado(0))
        self.connect(self.botonNotas, SIGNAL("clicked()"),
            lambda: self.item_cambiado(1))
        self.connect(boton_cerrar, SIGNAL("clicked()"),
            self.hide)

    def item_cambiado(self, v):
        if not self.isVisible():
            self.show()

        self.stack.show_display(v)

    def compilar_archivo(self, salida, path):
        self.item_cambiado(0)
        self.show()
        self.s = salida
        self.path = path
        self.salida_.correr_compilacion(self.s, self.path)

    def ejecutar_archivo(self):
        self.salida_.correr_programa()


class Notas(QTextEdit):

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setText(self.trUtf8("Acá puedes escribir notas..."))


class Stacked(QStackedWidget):

    def __init__(self):
        QStackedWidget.__init__(self)

    def setCurrentIndex(self, index):
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)