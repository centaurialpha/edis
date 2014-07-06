#-*- coding: utf-8 -*-
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

        logo_edis = QPixmap(recursos.ICONOS['seiryu'])
        self.logo_ = QLabel()
        self.logo_.setPixmap(logo_edis)
        self.logo_.setAlignment(Qt.AlignCenter)
        layoutV.addWidget(self.logo_)