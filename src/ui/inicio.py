# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser

from PyQt4.QtGui import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFont,
    QFrame,
    QPushButton,
    QListWidget,
    QDialog,
    QPixmap,
    QIcon
    )
from PyQt4.QtCore import Qt

from src.ui.edis_main import EDIS
from src import recursos
from src.helpers import configuraciones
from src import ui


class Inicio(QDialog):

    def __init__(self, parent=None):
        super(Inicio, self).__init__(parent, Qt.Dialog)
        contenedor = QVBoxLayout(self)
        self.setMinimumWidth(500)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        lbl_titulo = QLabel(self.tr("Bienvenido a EDIS..."))
        lbl_titulo.setFont(QFont("Consolas", 20))
        hbox.addWidget(lbl_titulo)
        hbox.addStretch(1)

        icono = QLabel()
        icono.setScaledContents(True)
        icono.setPixmap(QPixmap(recursos.ICONOS['explore']))
        hbox.addWidget(icono)

        frame = QFrame()
        frame.setStyleSheet("background: gray")
        frame.setFrameShape(frame.HLine)
        frame.setFrameShadow(frame.Plain)

        contenedor.addLayout(hbox)
        contenedor.addWidget(frame)

        lbl_texto = QLabel(self.tr("Acá alguna descripción"))
        lbl_texto.setWordWrap(True)
        lbl_texto.setFont(QFont("Consolas", 10))
        contenedor.addWidget(lbl_texto)

        contenedor.addWidget(QLabel("<b>Archivos en la última sesión:</b>"))

        lista_archivos = QListWidget()
        #FIXME: debería agregar los proyectos recientes y no los archivos
        recientes = configuraciones.RECIENTES
        if recientes is not None:
            for reciente in recientes:
                lista_archivos.addItem(reciente)
        contenedor.addWidget(lista_archivos)

        frame = QFrame()
        frame.setStyleSheet("background: gray")
        frame.setFrameShape(frame.HLine)
        frame.setFrameShadow(frame.Plain)

        contenedor.addWidget(frame)

        box_botones = QHBoxLayout()

        btn_abrir = QPushButton(self.tr("Abrir"))
        btn_abrir.setIcon(QIcon(recursos.ICONOS['open-small']))
        btn_nuevo = QPushButton(self.tr("Nuevo"))
        btn_nuevo.setIcon(QIcon(recursos.ICONOS['new-small']))
        btn_edis = QPushButton(self.tr("Edis web"))
        btn_edis.setIcon(QIcon(recursos.ICONOS['web']))
        box_botones.addWidget(btn_edis)
        box_botones.addStretch(1)
        box_botones.addWidget(btn_abrir)
        box_botones.addWidget(btn_nuevo)

        contenedor.addLayout(box_botones)

        EDIS.cargar_componente("inicio", self)
        # Conexiones
        btn_edis.clicked.connect(self._open_web)
        btn_abrir.clicked.connect(self._abrir)
        btn_nuevo.clicked.connect(self._nuevo)

    def _open_web(self):
        webbrowser.open_new(ui.__codigo_fuente__)

    def _abrir(self):
        principal = EDIS.componente("principal")
        principal.abrir_archivo()
        self.close()

    def _nuevo(self):
        principal = EDIS.componente("principal")
        principal.agregar_editor()
        self.close()


inicio = Inicio()