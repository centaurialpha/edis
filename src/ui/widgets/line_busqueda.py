# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QIcon

# Módulos QtCore
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt

# Módulos EDIS
from src import recursos
from src.ui.widgets import creador_widget
from src.ui.contenedor_principal import contenedor_principal


class Widget(QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.linea_busqueda = LineBusqueda()
        self.linea_linea = LineLinea()
        boton_buscar = QToolButton()
        boton_buscar.setAutoRaise(True)
        boton_buscar.setIcon(QIcon(recursos.ICONOS['buscar-tool']))
        boton_buscar_linea = QToolButton()
        boton_buscar_linea.setAutoRaise(True)
        boton_buscar_linea.setIcon(QIcon(recursos.ICONOS['ir-linea']))
        hbox.addWidget(self.linea_busqueda)
        hbox.addWidget(boton_buscar)
        hbox.addWidget(self.linea_linea)
        hbox.addWidget(boton_buscar_linea)
        hbox.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
            QSizePolicy.Expanding))

        self.setLayout(hbox)

        # Conexión
        boton_buscar.clicked.connect(self.linea_busqueda.buscar)
        boton_buscar_linea.clicked.connect(self.linea_linea.buscar_linea)


class LineBusqueda(QLineEdit):
    #FIXME
    def __init__(self):
        super(LineBusqueda, self).__init__()
        self.setPlaceholderText(self.trUtf8("Búsqueda rápida!"))
        self.setMaximumSize(QSize(200, 29))
        self.boton = QToolButton(self)
        self.boton.setAutoRaise(True)
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
        self.setPlaceholderText(self.trUtf8("Saltar"))
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