#-*- coding: utf-8 -*-

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPushButton

from PyQt4.QtCore import SIGNAL

from side_c import recursos

_instanciaBarraDeEstado = None


def BarraDeEstado(*args, **kw):
    global _instanciaBarraDeEstado
    if _instanciaBarraDeEstado is None:
        _instanciaBarraDeEstado = _BarraDeEstado(*args, **kw)

    return _instanciaBarraDeEstado


class _BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)

        self.widget = QWidget()

        v_layout = QVBoxLayout(self.widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        self.buscador = WidgetBuscar(self)
        self.addWidget(self.buscador)

        self.connect(self, SIGNAL("messageChanged(QString)"),
            self.mensaje_terminado)

        self.addWidget(self.widget)

    def showMessage(self, mensaje, tiempo):
        self.widget.hide()
        QStatusBar.showMessage(self, mensaje, tiempo)

    def mensaje_terminado(self, mensaje):
        if not mensaje:
            self.hide()


class WidgetBuscar(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent

        layoutH = QHBoxLayout(self)
        layoutH.setContentsMargins(0, 0, 0, 0)

        self.lineText = QLineEdit()
        self.lineText.setMaximumWidth(200)

        self.boton_buscar = QPushButton(QIcon(
            recursos.ICONOS['buscar']), '')

        layoutH.addWidget(self.lineText)
        layoutH.addWidget(self.boton_buscar)

        self.connect(self.boton_buscar, SIGNAL("clicked()"),
            self.buscar_texto)

    def buscar_texto(self):
        pass