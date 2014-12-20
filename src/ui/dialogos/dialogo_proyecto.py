# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QFileDialog
    )

from PyQt4.QtCore import pyqtSignal


class DialogoProyecto(QDialog):

    proyecto_listo = pyqtSignal(dict)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Proyecto nuevo"))
        self.resize(500, 100)
        contenedor = QVBoxLayout(self)
        contenedor.setContentsMargins(5, 5, 5, 5)
        form = QFormLayout()

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
        self.nombre_proyecto = self.line_nombre.text()
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
        self.close()
        # Se emite la señal con los datos del proyecto
        self.proyecto_listo.emit(datos)