# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import json

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QFileDialog,
    QMessageBox,
    )

from PyQt4.QtCore import (
    QThread
    )

from src.helpers import logger
from src.ui.edis_main import EDIS
log = logger.edisLogger("creador_proyecto")


#TODO: Esto todavía está incompleto


class DialogoProyecto(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Proyecto nuevo"))
        self.resize(500, 100)
        contenedor = QVBoxLayout(self)
        contenedor.setContentsMargins(5, 5, 5, 5)
        form = QFormLayout()

        # Thread
        self.creador_proyecto = CreadorProyectoThread()
        self.creador_proyecto.finished.connect(self._finalizar_thread)

        self.line_nombre = QLineEdit()
        self.line_nombre.setText("ProyectoNuevo")
        form.addRow(self.tr("Nombre:"), self.line_nombre)

        widget_ubicacion = QWidget()
        hbox = QHBoxLayout(widget_ubicacion)
        hbox.setMargin(0)
        self.line_ubicacion = QLineEdit()
        btn_ubicacion = QPushButton("...")
        btn_ubicacion.setStyleSheet("min-width: 25px; min-height: 10")
        hbox.addWidget(self.line_ubicacion)
        hbox.addWidget(btn_ubicacion)

        form.addRow(self.tr("Ubicación:"), widget_ubicacion)

        contenedor.addLayout(form)
        contenedor.addStretch(1)

        box_botones = QHBoxLayout()
        box_botones.addStretch(1)
        self.btn_aceptar = QPushButton(self.tr("Aceptar"))
        self.btn_aceptar.setDisabled(True)
        box_botones.addWidget(self.btn_aceptar)
        btn_cancelar = QPushButton(self.tr("Cancelar"))
        box_botones.addWidget(btn_cancelar)

        contenedor.addLayout(box_botones)

        # Conexiones
        btn_ubicacion.clicked.connect(self._seleccionar_carpeta)
        btn_cancelar.clicked.connect(self.close)
        self.line_nombre.textChanged.connect(self._validar)
        self.btn_aceptar.clicked.connect(self._enviar_datos)

        self._validar()

    def _seleccionar_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(self,
            self.tr("Selecciona la carpeta"))
        if carpeta:
            self.line_ubicacion.setText(carpeta)
        self._validar()

    def _validar(self):
        self.nombre_proyecto = self.line_nombre.text().replace(' ', '_')
        self.ubicacion_proyecto = self.line_ubicacion.text()
        if not self.ubicacion_proyecto:
            self.btn_aceptar.setDisabled(True)
            return
        elif not self.nombre_proyecto:
            self.btn_aceptar.setDisabled(True)
            return
        self.btn_aceptar.setDisabled(False)

    def _enviar_datos(self):
        datos = {
            'nombre': self.nombre_proyecto,
            'ubicacion': self.ubicacion_proyecto
            }
        self.creador_proyecto.crear(datos)

    def _finalizar_thread(self):
        if not self.creador_proyecto.error:
            principal = EDIS.componente('principal')
            principal.abrir_archivo(os.path.join(
                                    self.ubicacion_proyecto,
                                    self.nombre_proyecto, 'main.c'))
            self.close()
            #FIXME:
        else:
            QMessageBox.critical(self, self.tr("Errror"),
                            self.tr("Error al crear el proyecto\n\n%s") %
                            self.creador_proyecto.error)


class CreadorProyectoThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.error = False

    def run(self):
        try:
            # Se crea el directorio
            carpeta_proyecto = os.path.join(self._datos['ubicacion'],
                                            self._datos['nombre'])
            os.mkdir(carpeta_proyecto)
            # Se crea el archivo .epf (Edis Project File)
            archivo_epf = self._datos['nombre'] + '.epf'
            with open(os.path.join(carpeta_proyecto,
                        archivo_epf.lower()), mode='w') as archivo:
                json.dump(self._datos, archivo, indent=4)
            # Archivo main.c
            open(os.path.join(carpeta_proyecto, 'main.c'), 'w').close()
        except Exception as error:
            self.error = error

    def crear(self, proyecto):
        self._datos = proyecto
        # Run !
        self.start()