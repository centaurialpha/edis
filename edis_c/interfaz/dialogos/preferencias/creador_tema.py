#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QColorDialog

from PyQt4.QtCore import QString

from edis_c import recursos
from edis_c.interfaz.contenedor_principal import contenedor_principal


class CreadorDeTemaEditor(QWidget):

    def __init__(self, parent):
        super(CreadorDeTemaEditor, self).__init__()
        self.parent = parent
        layoutV = QVBoxLayout(self)
        scroll = QScrollArea()
        layoutV.addWidget(scroll)

        self.linea_palabraReservada = QLineEdit()
        boton_palabraReservada = QPushButton(self.trUtf8("Color"))
        self.linea_numero = QLineEdit()
        boton_numero = QPushButton(self.trUtf8("Color"))
        self.linea_include = QLineEdit()
        boton_include = QPushButton(self.trUtf8("Color"))
        self.linea_comentario = QLineEdit()
        boton_comentario = QPushButton(self.trUtf8("Color"))
        self.linea_cadena = QLineEdit()
        boton_cadena = QPushButton(self.trUtf8("Color"))
        self.linea_braces = QLineEdit()
        boton_braces = QPushButton(self.trUtf8("Color"))

        layoutH = QHBoxLayout()
        layoutH.addWidget(QLabel(self.trUtf8("Nombre:")))
        self.linea_nombre = QLineEdit()
        layoutH.addWidget(self.linea_nombre)
        boton_guardarTema = QPushButton(self.trUtf8("Guardar tema!"))
        layoutH.addWidget(boton_guardarTema)

        grilla = QGridLayout()
        grilla.addWidget(QLabel(self.trUtf8("Palabra reservada:")), 0, 0)
        grilla.addWidget(self.linea_palabraReservada, 0, 1)
        grilla.addWidget(boton_palabraReservada, 0, 2)
        grilla.addWidget(QLabel(self.trUtf8("Número:")), 1, 0)
        grilla.addWidget(self.linea_numero, 1, 1)
        grilla.addWidget(boton_numero, 1, 2)
        grilla.addWidget(QLabel(self.trUtf8("Include:")), 2, 0)
        grilla.addWidget(self.linea_include, 2, 1)
        grilla.addWidget(boton_include, 2, 2)
        grilla.addWidget(QLabel(self.trUtf8("Comentario:")), 3, 0)
        grilla.addWidget(self.linea_comentario, 3, 1)
        grilla.addWidget(boton_comentario, 3, 2)
        grilla.addWidget(QLabel(self.trUtf8("Cadena:")), 4, 0)
        grilla.addWidget(self.linea_cadena, 4, 1)
        grilla.addWidget(boton_cadena, 4, 2)
        grilla.addWidget(QLabel(self.trUtf8("Braces:")), 5, 0)
        grilla.addWidget(self.linea_braces, 5, 1)
        grilla.addWidget(boton_braces, 5, 2)

        frame = QFrame()
        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH)
        layoutV.addLayout(grilla)
        frame.setLayout(layoutV)
        scroll.setWidget(frame)

        # Color de botón obtenido del texto.
        self.linea_palabraReservada.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_palabraReservada,
                self.linea_palabraReservada.text()))
        self.linea_numero.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numero, self.linea_numero.text()))
        self.linea_include.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_include, self.linea_include.text()))
        self.linea_comentario.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_comentario,
                self.linea_comentario.text()))
        self.linea_cadena.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_cadena, self.linea_cadena.text()))
        self.linea_braces.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_braces, self.linea_braces.text()))

        # Elección de color
        boton_palabraReservada.clicked.connect(lambda: self.elegir_color(
            self.linea_palabraReservada, boton_palabraReservada))

    def aplicar_estilo_de_color(self):
        self.linea_palabraReservada.setText(
            recursos.NUEVO_TEMA.get('palabra',
                recursos.TEMA_EDITOR['palabra']))
        self.linea_numero.setText(recursos.NUEVO_TEMA.get('numero',
            recursos.TEMA_EDITOR['numero']))
        self.linea_include.setText(recursos.NUEVO_TEMA.get('include',
            recursos.TEMA_EDITOR['include']))
        self.linea_comentario.setText(recursos.NUEVO_TEMA.get('comentario',
            recursos.TEMA_EDITOR['comentario']))
        self.linea_cadena.setText(recursos.NUEVO_TEMA.get('cadena',
            recursos.TEMA_EDITOR['cadena']))
        self.linea_braces.setText(recursos.NUEVO_TEMA.get('braces',
            recursos.TEMA_EDITOR['braces']))

    def estilo_boton(self, boton, nombre):
        if QColor(nombre).isValid():
            boton.setAutoFillBackground(True)
            estilo = ('background: %s; border-radius: 5px; '
                        'padding: 5px;' % nombre)
            boton.setStyleSheet(estilo)

    def elegir_color(self, lineEdit, boton):
        color = QColorDialog.getColor(QColor(lineEdit.text()),
            self, self.trUtf8("Elige el color: "))
        if color.isValid():
            lineEdit.setText(str(color.name()))
            self.estilo_boton(boton, color.name())
            self.previsualizar()

    def showEvent(self, evento):
        super(CreadorDeTemaEditor, self).showEvent(evento)
        self.aplicar_estilo_de_color()
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        self.aplicar_estilo_de_color()

    def previsualizar(self):
        tema = {
            "palabra": str(self.linea_palabraReservada.text()),
            "numero": str(self.linea_numero.text()),
            "include": str(self.linea_include.text()),
            "comentario": str(self.linea_comentario.text()),
            "cadena": str(self.linea_cadena.text()),
            "braces": str(self.linea_braces.text())
            }
        recursos.NUEVO_TEMA = tema
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        return tema