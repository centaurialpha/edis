#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
#from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTabBar
from PyQt4.QtGui import QStylePainter
from PyQt4.QtGui import QStyleOptionTab
from PyQt4.QtGui import QStyle
#from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSpacerItem


from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QProcess

#from side_c import recursos
from edis_c.interfaz.contenedor_secundario import salida_widget
from edis_c.nucleo import configuraciones

if configuraciones.LINUX is not False:
    from PyQt4.QtGui import QX11EmbedContainer


_instanciaContenedorSecundario = None


def ContenedorBottom(*args, **kw):
    global _instanciaContenedorSecundario
    if _instanciaContenedorSecundario is None:
        _instanciaContenedorSecundario = _ContenedorBottom(*args, **kw)

    return _instanciaContenedorSecundario


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


class _ContenedorBottom(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(10)
        vlayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding))

        self.salida_ = salida_widget.EjecutarWidget()
        self.notas = Notas(self)

        self.tabs = QTabWidget(self)
        self.tabs.setTabBar(Tab(ancho=55, alto=35))

        #if configuraciones.LINUX is not False:
         #   self.term = Terminal(self)
          #  self.agregar_tab(self.term, "")

        self.agregar_tab(self.salida_, "Salida")
        self.agregar_tab(self.notas, "Notas")
        self.tabs.setTabPosition(QTabWidget.East)

        hlayout = QHBoxLayout()
        vlayout.addWidget(self.tabs)
        vlayout.addLayout(hlayout)

    def agregar_tab(self, widget, titulo):
        self.tabs.addTab(widget, titulo)

    def compilar_archivo(self, salida, path):
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


class Terminal(QWidget):
    """ Terminal embebida (xterm) """

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.proceso = QProcess(self)
        self.terminal = QX11EmbedContainer(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        #layout.setStretch(300, 300)
        layout.addWidget(self.terminal)

        import sys

        try:

            if sys.platform == configuraciones.TUX:
                self.proceso.start('xterm',
                    ['-into', str(self.terminal.winId())])

        except:
            pass