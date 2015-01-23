# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QStatusBar,
    QWidget,
    QHBoxLayout,
    QLabel
    )

from PyQt4.QtCore import QTimer

from src.ui.edis_main import EDIS


class BarraDeEstado(QStatusBar):

    def __init__(self, parent=None):
        super(BarraDeEstado, self).__init__()
        # Widgets
        self.cursor_widget = PosicionCursorWidget()
        self.uptime_widget = UpTimeWidget()
        self.lbl_archivo = QLabel(self.tr(""))
        # Contenedor
        contenedor = QWidget()
        box = QHBoxLayout(contenedor)
        box.setContentsMargins(0, 0, 10, 0)
        box.addWidget(self.cursor_widget)
        box.addWidget(self.uptime_widget)

        # Agregar contenedor al status bar
        self.addWidget(self.lbl_archivo)
        self.addPermanentWidget(contenedor)

        EDIS.cargar_componente("barra_de_estado", self)

    def path_archivo(self, path):
        self.lbl_archivo.setText(path)


class PosicionCursorWidget(QLabel):

    def __init__(self):
        super(PosicionCursorWidget, self).__init__()
        self.setObjectName("status_label")
        self.setStyleSheet("font: 10pt;")
        self.linea_columna = "Línea %s, Columna %s - " \
        "<span style='color: #aaaaaa;'>%s líneas</span>"
        self.setText(self.tr(self.linea_columna % (0, 0, 0)))

    def actualizar_cursor(self, linea, columna, lineas):
        self.setText(self.linea_columna % (linea, columna, lineas))


class UpTimeWidget(QLabel):

    def __init__(self):
        super(UpTimeWidget, self).__init__()
        self.setObjectName("status_label")
        self.setStyleSheet("font: 10pt;")
        # Inicio
        self.tiempo = 0

        self.lbl_tiempo = "Tiempo: %smin"
        self.setText(self.tr(self.lbl_tiempo % (0)))

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.timer.start()

    def actualizar_tiempo(self):
        """ Actualiza el label cada 60 segundos """

        self.tiempo += 1
        if self.tiempo == 60:
            tiempo = "1hr"
        elif self.tiempo > 60:
            horas = int(str(self.tiempo / 60).split('.')[0])
            hora = str(horas) + "hs"
            minutos = str(self.tiempo - (horas * 60)) + "min"
            tiempo = hora + minutos
        else:
            tiempo = str(self.tiempo) + "min"
        self.setText(self.tr("Tiempo: %s" % tiempo))


barra_de_estado = BarraDeEstado()