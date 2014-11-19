# -*- coding: utf-8 -*-

# <Barra de estado, muestra statustips y eventos que ocurren en el editor.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

# Módulos QtGui
from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QProgressBar
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel

# Módulos QtCore
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

# Módulos EDIS
from src.ui.editor import acciones_
from src.ui.contenedor_secundario import contenedor_secundario

_instanciaBarraDeEstado = None


def BarraDeEstado(*args, **kw):
    global _instanciaBarraDeEstado
    if _instanciaBarraDeEstado is None:
        _instanciaBarraDeEstado = _BarraDeEstado(*args, **kw)

    return _instanciaBarraDeEstado


class _BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()
        self.widget_ = QWidget()

        layout = QGridLayout(self.widget)
        layout_ = QGridLayout(self.widget_)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_.setContentsMargins(100, 0, 0, 0)
        layout_.setSpacing(0)
        layout.setSpacing(0)
        self.linea_columna = EstadoLineaColumna(self)
        layout.addWidget(self.linea_columna, 0, 0)
        self.user_host = UserHost(self)

        layout_.addWidget(self.user_host, 3, 1, alignment=Qt.AlignRight)
        self.connect(self, SIGNAL("messageChanged(QString)"),
                     self.mensaje_terminado)

        self.addWidget(self.linea_columna, Qt.AlignLeft)
        self.addWidget(self.user_host, Qt.AlignRight)

    def showMessage(self, mensaje, tiempo):
        """ @mensaje: texto QString que será mostrado en la barra de estado.
            @tiempo: tiempo en milisegundos que se mostrará el mensaje.
        """

        self.linea_columna.hide()
        QStatusBar.showMessage(self, mensaje, tiempo)

    def mensaje_terminado(self, mensaje):
        if not mensaje:
            self.linea_columna.show()


class EstadoLineaColumna(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.parent = parent

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        self.texto = "Linea: <b>%s</b> / <b>%s</b> | Columna:<b>%s</b>"
        self.posicion_cursor = QLabel(self.trUtf8(
            self.texto % (0, 0, 0)))

        layoutH.addWidget(self.posicion_cursor)

        layoutV.addLayout(layoutH)

    def actualizar_linea_columna(self, linea, total, columna):
        """ Actualiza la barra de estado con linea, columna
        y total de líneas.
        """

        self.posicion_cursor.setText(
            self.trUtf8(self.texto % (linea, total, columna)))


class UserHost(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.parent = parent

        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        self.user_host = "user_name: <b>%s</b>  hostname: <b>%s</b>"
        self.label = QLabel(self.trUtf8(
            self.user_host % (0, 0)))

        layoutH.addWidget(self.label)
        layoutV.addLayout(layoutH)

        self.obtener_texto()

    def obtener_texto(self):
        """ Obtiene el nombre de usuario y máquina del sistema.  """

        texto = acciones_.obtener_user_hostname()
        self.texto_user_host(texto[0], texto[1])

    def texto_user_host(self, username, hostname):
        """ Coloca el nombre de usuario y máquina obtenido por el método
        obtener_texto.
        """

        self.label.setText(self.trUtf8(self.user_host % (username, hostname)))


class BarraDeProgreso(QProgressBar):

    def __init__(self, parent):
        super(BarraDeProgreso, self).__init__(parent)
        self.setMaximumWidth(150)
        self.setValue(20)
        self.salida = contenedor_secundario.salida_widget.EjecutarWidget()
