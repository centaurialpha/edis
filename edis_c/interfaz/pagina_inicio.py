#-*- coding: utf-8 -*-

# <Widget que muestra la página de inicio de EDIS.>
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

""" Página de inicio """

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPixmap

from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.interfaz import tabitem


class PaginaDeInicio(QWidget, tabitem.TabItem):

    def __init__(self, parent=None):
        super(PaginaDeInicio, self).__init__(parent)
        self._id = "Pagina de Inicio"
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        titulo_label = QLabel(self.trUtf8(
            "<h1>Bienvenido a EDIS-C</h1> <i>Seiryü</i>"))
        titulo_label.setAlignment(Qt.AlignCenter)
        logo_edis = QPixmap(recursos.ICONOS['seiryu'])
        self.logo_ = QLabel()
        self.logo_.setPixmap(logo_edis)
        self.logo_.setAlignment(Qt.AlignCenter)

        descripcion = QLabel(self.trUtf8("""
        <b>EDIS-C</b> es una plataforma de Software Libre para el desarrollo de
        programas con el lenguaje C.<br>
        Está programado en <i>Python</i> y <i>Qt (PyQt)</i>.<br><br>"""))
        tips = QLabel(self.trUtf8("""
        <hr /><UL type=disk><LI>Presiona <i>Ctrl+N</i> para comenzar a \
        escribir un nuevo archivo.<LI>Para mayor legibilidad de tu código \
        puedes aplicarle o sacarle indentación con <i>TAB y Shift+TAB \
        respectivamente.</i><Li>Mueve hacia abajo o arriba una o más \
        lineas de código con <i>ALT+Flecha arria o abajo.</i>\
        <LI>Inserta un título o separador desde el menú \
        <i>Insertar.</i><hr /></UL>
        """))
        reportar_b = QLabel(self.trUtf8("""
        <h6>Si encuentras algún error en el programa o deseas una nueva \
característica, por favor comunícala desde el menú \
<i>Acerca de/Reportar bugs</i>.</h6>
        """))
        reportar_b.setAlignment(Qt.AlignBottom)
        descripcion.setAlignment(Qt.AlignCenter)
        layoutV.addWidget(titulo_label)
        layoutV.addWidget(self.logo_)
        layoutV.addWidget(descripcion)
        layoutV.addWidget(tips)
        layoutV.addWidget(reportar_b)