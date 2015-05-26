# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QStatusBar,
    #QWidget,
    #QHBoxLayout,
    #QLabel
    )

#from PyQt4.QtCore import QTimer

from src.ui.main import Edis


class StatusBar(QStatusBar):
    """ Implementación de Barra de Estado """

    def __init__(self):
        QStatusBar.__init__(self)
        self.hide()
        Edis.load_component("status_bar", self)

        # Conexiones
        self.messageChanged.connect(self._clean_status)

    def _clean_status(self, msg):
        if not msg:
            self.hide()

    def show_message(self, msg):
        self.show()
        self.showMessage(self.tr("Archivo guardado: {0}").format(msg), 4000)


status_bar = StatusBar()

#class BarraDeEstado(QStatusBar):

    #def __init__(self, parent=None):
        #super(BarraDeEstado, self).__init__()
        ## Widgets
        #self.uptime_widget = UpTimeWidget()
        #self.lbl_archivo = QLabel(self.tr(""))
        ## Contenedor
        #contenedor = QWidget()
        #box = QHBoxLayout(contenedor)
        #box.setContentsMargins(0, 0, 10, 0)
        ## box.addWidget(self.cursor_widget)
        #box.addWidget(self.uptime_widget)

        ## Agregar contenedor al status bar
        #self.addWidget(self.lbl_archivo)
        #self.addPermanentWidget(contenedor)

        #Edis.load_component("status_bar", self)

    #def update_status(self, filename):
        #self.lbl_archivo.setText(filename)


#class UpTimeWidget(QLabel):

    #def __init__(self):
        #super(UpTimeWidget, self).__init__()
        #self.setObjectName("status_label")
        #self.setStyleSheet("font: 10pt;")
        ## Inicio
        #self.tiempo = 0

        #self.setText("Uptime: {0}min".format(self.tiempo))

        ## Timer
        #self.timer = QTimer()
        #self.timer.setInterval(60000)
        #self.timer.timeout.connect(self.update_time)
        #self.timer.start()

    #def update_time(self):
        #""" Actualiza el label cada 60 segundos """

        #self.tiempo += 1
        #if self.tiempo == 60:
            #tiempo = "1hr"
        #elif self.tiempo > 60:
            #horas = int(str(self.tiempo / 60).split('.')[0])
            #hora = str(horas) + "hs"
            #minutos = str(self.tiempo - (horas * 60)) + "min"
            #tiempo = hora + minutos
        #else:
            #tiempo = str(self.tiempo) + "min"
        #self.setText("Uptime: {0}".format(tiempo))