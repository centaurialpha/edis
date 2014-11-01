# -*- coding: utf-8 -*-

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


from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QPushButton,
    QAbstractItemView,
    QLabel,
    QShortcut,
    QKeySequence
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from edis.interfaz.contenedor_principal import contenedor_principal


class Dialogo(QDialog):

    def __init__(self, archivos):
        super(Dialogo, self).__init__()
        self.setWindowTitle(self.tr("Archivos sin guardar!"))
        self.evento_ignorado = False

        linea = QFrame()
        linea.setFrameStyle(QFrame.VLine | QFrame.Sunken)

        vLayout = QVBoxLayout()
        label = QLabel(self.tr("Algunos archivos no se han guardado,\n"
                        "selecciona los que deseas guardar:"))
        vLayout.addWidget(label)
        self.lista = QListWidget()
        [self.lista.addItem(item) for item in archivos]
        self.lista.setSelectionMode(QAbstractItemView.ExtendedSelection)
        vLayout.addWidget(self.lista)

        layoutBotones = QVBoxLayout()
        botonTodo = QPushButton(self.tr("Seleccionar todo"))
        botonNinguno = QPushButton(self.tr("Seleccionar ninguno"))
        botonGuardar = QPushButton(self.tr("Guardar"))
        botonCancelar = QPushButton(self.tr("Cancelar"))
        botonNoGuardar = QPushButton(self.tr("No guardar"))
        layoutBotones.addWidget(botonTodo)
        layoutBotones.addWidget(botonNinguno)
        layoutBotones.addWidget(botonGuardar)
        layoutBotones.addWidget(botonCancelar)
        layoutBotones.addWidget(botonNoGuardar)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addWidget(linea)
        layout.addLayout(layoutBotones)
        self.setLayout(layout)

        self.tecla_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self.tecla_escape, SIGNAL("activated()"), self.ignorar)
        self.connect(botonTodo, SIGNAL("clicked()"), self.seleccionar_todo)
        self.connect(botonNinguno, SIGNAL("clicked()"), self.deseleccionar)
        self.connect(botonGuardar, SIGNAL("clicked()"), self.guardar)
        self.connect(botonNoGuardar, SIGNAL("clicked()"), self.close)
        self.connect(botonCancelar, SIGNAL("clicked()"), self.ignorar)

    def ignorar(self):
        self.evento_ignorado = True
        self.hide()

    def ignorado(self):
        return self.evento_ignorado

    def seleccionar_todo(self):
        for item in range(self.lista.count()):
            self.lista.item(item).setSelected(True)

    def deseleccionar(self):
        for item in range(self.lista.count()):
            self.lista.item(item).setSelected(False)

    def guardar(self):
        archivos_seleccionados = self.lista.selectedItems()
        for archivo in archivos_seleccionados:
            nombre = archivo.text()
            contenedor_principal.ContenedorMain().guardar_seleccionado(nombre)
        self.close()