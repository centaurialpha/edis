# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
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


class Dialogo(QDialog):

    def __init__(self, archivos, principal):
        super(Dialogo, self).__init__(principal)
        self.setWindowTitle(self.tr("Archivos sin guardar!"))
        self.principal = principal
        self.evento_ignorado = False

        vLayout = QVBoxLayout(self)
        label = QLabel(self.tr("Algunos archivos no se han guardado, "
                       "selecciona los que \ndeseas guardar:"))
        vLayout.addWidget(label)
        hLayout = QHBoxLayout()

        self.lista = QListWidget()
        [self.lista.addItem(item) for item in archivos]
        self.lista.setSelectionMode(QAbstractItemView.ExtendedSelection)
        hLayout.addWidget(self.lista)

        layoutBotones = QVBoxLayout()
        botonTodo = QPushButton(self.tr("Todo"))
        botonNinguno = QPushButton(self.tr("Ninguno"))
        botonGuardar = QPushButton(self.tr("Guardar"))
        botonCancelar = QPushButton(self.tr("Cancelar"))
        botonNoGuardar = QPushButton(self.tr("No guardar"))
        layoutBotones.addWidget(botonTodo)
        layoutBotones.addWidget(botonNinguno)
        layoutBotones.addWidget(botonGuardar)
        layoutBotones.addWidget(botonNoGuardar)
        layoutBotones.addWidget(botonCancelar)

        hLayout.addLayout(layoutBotones)
        vLayout.addLayout(hLayout)

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
            self.principal.guardar_seleccionado(nombre)
        self.close()