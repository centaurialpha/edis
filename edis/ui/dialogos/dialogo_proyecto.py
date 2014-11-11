# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QToolButton
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt,
    QSize
    )

from edis_c.ui.widgets import creador_widget


class DialogoProyecto(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setWindowTitle(self.trUtf8("EDIS - Proyecto nuevo"))
        boxV = QVBoxLayout(self)

        boxH = QHBoxLayout()
        boxH.addWidget(QLabel(self.trUtf8("Nombre del proyecto:")))
        self.lineNombre = QLineEdit()
        boxH.addWidget(self.lineNombre)

        boxHH = QHBoxLayout()
        boxHH.addWidget(QLabel(self.trUtf8("Seleccione la carpeta:")))
        self.lineExaminar = QLineEdit()
        self.botonLimpiar = QToolButton(self)
        self.botonLimpiar.setAutoRaise(True)
        self.botonLimpiar.setIcon(
            creador_widget.get_icono_estandard("TitleBarCloseButton"))
        layoutLine = QHBoxLayout(self.lineNombre)
        layoutLine.addWidget(self.botonLimpiar, 2, Qt.AlignRight)
        self.lineExaminar.setReadOnly(True)
        boxHH.addWidget(self.lineExaminar)
        self.botonExaminar = QPushButton(self.trUtf8("..."))
        self.botonExaminar.setMaximumSize(QSize(25, 25))
        boxHH.addWidget(self.botonExaminar)

        boxBotones = QHBoxLayout()
        self.botonAceptar = QPushButton(self.trUtf8("Aceptar"))
        self.botonCancelar = QPushButton(self.trUtf8("Cancelar"))
        boxBotones.addWidget(self.botonCancelar)
        boxBotones.addWidget(self.botonAceptar)

        boxBotones.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
            QSizePolicy.Expanding))
        boxV.addLayout(boxH)
        boxV.addLayout(boxHH)
        boxV.addLayout(boxBotones)

        self.connect(self.botonExaminar, SIGNAL("clicked()"),
            self.seleccionar_carpeta)
        self.connect(self.botonCancelar, SIGNAL("clicked()"),
            self.close)
        self.connect(self.botonAceptar, SIGNAL("clicked()"),
            self.crear_proyecto)

    def seleccionar_carpeta(self):
        self.lineExaminar.setText(QFileDialog.getExistingDirectory(
            self, self.trUtf8("Selecciona la carpeta")))

    def crear_proyecto(self):
        nombre = self.lineNombre.text()
        carpeta = os.path.join(unicode(self.lineExaminar.text()),
            unicode(nombre))
        if not carpeta:
            return
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        self.close()