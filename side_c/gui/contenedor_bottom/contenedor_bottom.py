#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTabBar
from PyQt4.QtGui import QStylePainter
from PyQt4.QtGui import QStyleOptionTab
from PyQt4.QtGui import QStyle

from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt

from side_c import recursos


class Tab(QTabBar):
    """ Se colocan los tabs a la derecha y el texto en horizontal.
        https://gist.github.com/LegoStormtroopr/5075267

    """
    def __init__(self, *args, **kwargs):
        self.tam_tabs = QSize(kwargs.pop('ancho'), kwargs.pop('alto'))
        super(Tab, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QStylePainter()
        option = QStyleOptionTab()

        painter.begin(self)
        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, Qt.AlignVCenter | Qt.TextDontClip,
                             self.tabText(index))
        painter.end()

    def tabSizeHint(self, index):
        return self.tam_tabs


class ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        self.salida_ = SalidaWidget(self)
        self.notas = Notas(self)

        self.tabs = QTabWidget()
        self.tabs.setTabBar(Tab(ancho=60, alto=35))

        self.tabs.addTab(self.salida_, "Salida")
        self.tabs.addTab(self.notas, "Notas")

        self.tabs.setTabPosition(QTabWidget.East)

        hlayout = QHBoxLayout()
        vlayout.addWidget(self.tabs)
        vlayout.addLayout(hlayout)


class SalidaWidget(QPlainTextEdit):
    """ Widget que muestra stdin/stderr. """

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)

        self.parent = parent
        # Solo lectura
        self.setReadOnly(True)
        self.cargar_estilo()

    def cargar_estilo(self):
        tema = 'QPlainTextEdit {color: %s; background-color: %s;}' \
        % (recursos.COLOR_EDITOR['texto'], recursos.COLOR_EDITOR['fondo-input'])

        self.setStyleSheet(tema)


class Notas(QTextEdit):

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setText(self.trUtf8("Acá puedes escribir notas..."))
