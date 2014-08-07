#-*- coding: utf-8 -*-

#from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QToolButton

from PyQt4.QtCore import Qt

from edis_c.interfaz.widgets import creador_widget
from edis_c.interfaz.contenedor_principal import contenedor_principal


class LineBusqueda(QLineEdit):
    #FIXME
    def __init__(self):
        super(LineBusqueda, self).__init__()
        self.setPlaceholderText(self.trUtf8("Búsqueda rápida!"))
        self.setMaximumSize(QSize(200, 29))
        self.boton = QToolButton(self)
        self.boton.setCursor(Qt.PointingHandCursor)
        self.boton.setFocusPolicy(Qt.NoFocus)
        self.boton.setIcon(
            creador_widget.get_icono_estandard("DialogResetButton"))
        self.boton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        layout = QHBoxLayout(self)
        layout.addWidget(self.boton, 2, Qt.AlignRight)
        layout.setSpacing(0)
        layout.setMargin(2)

        self.returnPressed.connect(self.buscar)
        self.boton.clicked.connect(self.clear)

    def buscar(self):
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.buscar_match(unicode(self.text()), 0, True)


class LineLinea(QLineEdit):

    def __init__(self):
        super(LineLinea, self).__init__()
        self.setMaximumSize(QSize(100, 25))
        self.setPlaceholderText(self.trUtf8("Línea"))
        #self.setStyleSheet("")
        self.returnPressed.connect(self.buscar_linea)

    def buscar_linea(self):
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            maxx = Weditor.blockCount()
            linea = int(self.text())
            if maxx >= linea:
                cursor = Weditor.textCursor()
                cursor.setPosition(Weditor.document().findBlockByLineNumber(
                    linea - 1).position())
                Weditor.setTextCursor(cursor)
                self.setStyleSheet("color: gray;")
            else:
                self.setStyleSheet(
                    'background-color: rgb(255, 100, 10);border-radius: 3px;')
        Weditor.setFocus()