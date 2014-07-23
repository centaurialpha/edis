#-*- coding: utf-8 -*-
import copy

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
        layoutV.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        layoutV.addWidget(scroll)
        self.original = copy.copy(recursos.NUEVO_TEMA)

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
        self.linea_texto = QLineEdit()
        boton_texto = QPushButton(self.trUtf8("Color"))
        self.linea_fondoEditor = QLineEdit()
        boton_fondoEditor = QPushButton(self.trUtf8("Color"))
        self.linea_seleccion = QLineEdit()
        boton_seleccion = QPushButton(self.trUtf8("Color"))
        self.linea_fondoSeleccion = QLineEdit()
        boton_fondoSeleccion = QPushButton(self.trUtf8("Color"))
        self.linea_lineaActual = QLineEdit()
        boton_lineaActual = QPushButton(self.trUtf8("Color"))
        self.linea_sidebar = QLineEdit()
        boton_sidebar = QPushButton(self.trUtf8("Color"))
        self.linea_numeroLinea = QLineEdit()
        boton_numeroLinea = QPushButton(self.trUtf8("Color"))
        self.linea_numeroSeleccionado = QLineEdit()
        boton_numeroSeleccionado = QPushButton(self.trUtf8("Color"))
        self.linea_margen = QLineEdit()
        boton_margen = QPushButton(self.trUtf8("Color"))

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
        grilla.addWidget(QLabel(self.trUtf8("Texto editor:")), 6, 0)
        grilla.addWidget(self.linea_texto, 6, 1)
        grilla.addWidget(boton_texto, 6, 2)
        grilla.addWidget(QLabel(self.trUtf8("Fondo editor:")), 7, 0)
        grilla.addWidget(self.linea_fondoEditor, 7, 1)
        grilla.addWidget(boton_fondoEditor, 7, 2)
        grilla.addWidget(QLabel(self.trUtf8("Texto seleccionado:")), 8, 0)
        grilla.addWidget(self.linea_seleccion, 8, 1)
        grilla.addWidget(boton_seleccion, 8, 2)
        grilla.addWidget(QLabel(self.trUtf8("Fondo selección:")), 9, 0)
        grilla.addWidget(self.linea_fondoSeleccion, 9, 1)
        grilla.addWidget(boton_fondoSeleccion, 9, 2)
        grilla.addWidget(QLabel(self.trUtf8("Linea actual:")), 10, 0)
        grilla.addWidget(self.linea_lineaActual, 10, 1)
        grilla.addWidget(boton_lineaActual, 10, 2)
        grilla.addWidget(QLabel(self.trUtf8("Sidebar:")), 11, 0)
        grilla.addWidget(self.linea_sidebar, 11, 1)
        grilla.addWidget(boton_sidebar, 11, 2)
        grilla.addWidget(QLabel(self.trUtf8("Número sidebar:")), 12, 0)
        grilla.addWidget(self.linea_numeroLinea, 12, 1)
        grilla.addWidget(boton_numeroLinea, 12, 2)
        grilla.addWidget(QLabel(self.trUtf8("Número seleccionado:")), 13, 0)
        grilla.addWidget(self.linea_numeroSeleccionado, 13, 1)
        grilla.addWidget(boton_numeroSeleccionado, 13, 2)
        grilla.addWidget(QLabel(self.trUtf8("Márgen:")), 14, 0)
        grilla.addWidget(self.linea_margen, 14, 1)
        grilla.addWidget(boton_margen, 14, 2)

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
        self.linea_texto.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_texto, self.linea_texto.text()))
        self.linea_fondoEditor.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_fondoEditor,
                self.linea_fondoEditor.text()))
        self.linea_seleccion.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_seleccion,
                self.linea_seleccion.text()))
        self.linea_fondoSeleccion.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_fondoSeleccion,
                self.linea_fondoSeleccion.text()))
        self.linea_lineaActual.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_lineaActual,
                self.linea_lineaActual.text()))
        self.linea_sidebar.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_sidebar,
                self.linea_sidebar.text()))
        self.linea_numeroLinea.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numeroLinea,
                self.linea_numeroLinea.text()))
        self.linea_numeroSeleccionado.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numeroSeleccionado,
                self.linea_numeroSeleccionado.text()))
        self.linea_margen.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_margen,
                self.linea_margen.text()))

        # Elección de color
        boton_palabraReservada.clicked.connect(lambda: self.elegir_color(
            self.linea_palabraReservada, boton_palabraReservada))
        boton_numero.clicked.connect(lambda: self.elegir_color(
            self.linea_numero, boton_numero))
        boton_include.clicked.connect(lambda: self.elegir_color(
            self.linea_include, boton_include))
        boton_comentario.clicked.connect(lambda: self.elegir_color(
            self.linea_comentario, boton_comentario))
        boton_cadena.clicked.connect(lambda: self.elegir_color(
            self.linea_cadena, boton_cadena))
        boton_braces.clicked.connect(lambda: self.elegir_color(
            self.linea_braces, boton_braces))
        boton_texto.clicked.connect(lambda: self.elegir_color(
            self.linea_texto, boton_texto))
        boton_fondoEditor.clicked.connect(lambda: self.elegir_color(
            self.linea_fondoEditor, boton_fondoEditor))
        boton_seleccion.clicked.connect(lambda: self.elegir_color(
            self.linea_seleccion, boton_seleccion))
        boton_fondoSeleccion.clicked.connect(lambda: self.elegir_color(
            self.linea_fondoSeleccion, boton_fondoSeleccion))
        boton_lineaActual.clicked.connect(lambda: self.elegir_color(
            self.linea_lineaActual, boton_lineaActual))
        boton_sidebar.clicked.connect(lambda: self.elegir_color(
            self.linea_sidebar, boton_sidebar))
        boton_numeroLinea.clicked.connect(lambda: self.elegir_color(
            self.linea_numeroLinea, boton_numeroLinea))
        boton_numeroSeleccionado.clicked.connect(lambda: self.elegir_color(
            self.linea_numeroSeleccionado, boton_numeroSeleccionado))
        boton_margen.clicked.connect(lambda: self.elegir_color(
            self.linea_margen, boton_margen))

        for i in range(0, 15):
            it = grilla.itemAtPosition(i, 1).widget()
            boton = grilla.itemAtPosition(i, 2).widget()
            it.returnPressed.connect(self.previsualizar)
            self.estilo_boton(boton, it.text())

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
        self.linea_texto.setText(recursos.NUEVO_TEMA.get('texto-editor',
            recursos.TEMA_EDITOR['texto-editor']))
        self.linea_fondoEditor.setText(recursos.NUEVO_TEMA.get('fondo-editor',
            recursos.TEMA_EDITOR['fondo-editor']))
        self.linea_seleccion.setText(recursos.NUEVO_TEMA.get('seleccion-editor',
            recursos.TEMA_EDITOR['seleccion-editor']))
        self.linea_fondoSeleccion.setText(
            recursos.NUEVO_TEMA.get('fondo-seleccion-editor',
                recursos.TEMA_EDITOR['fondo-seleccion-editor']))
        self.linea_lineaActual.setText(recursos.NUEVO_TEMA.get('linea-actual',
            recursos.TEMA_EDITOR['linea-actual']))
        self.linea_sidebar.setText(recursos.NUEVO_TEMA.get('widget-num-linea',
            recursos.TEMA_EDITOR['widget-num-linea']))
        self.linea_numeroLinea.setText(recursos.NUEVO_TEMA.get('numero-linea',
            recursos.TEMA_EDITOR['numero-linea']))
        self.linea_numeroSeleccionado.setText(
            recursos.NUEVO_TEMA.get('num-seleccionado',
                recursos.TEMA_EDITOR['num-seleccionado']))
        self.linea_margen.setText(recursos.NUEVO_TEMA.get('margen-linea',
            recursos.TEMA_EDITOR['margen-linea']))

    def estilo_boton(self, boton, nombre):
        """ Pinta los botones """

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

    def previsualizar(self):
        tema = {
            "palabra": str(self.linea_palabraReservada.text()),
            "numero": str(self.linea_numero.text()),
            "include": str(self.linea_include.text()),
            "comentario": str(self.linea_comentario.text()),
            "cadena": str(self.linea_cadena.text()),
            "braces": str(self.linea_braces.text()),
            "texto-editor": str(self.linea_texto.text()),
            "fondo-editor": str(self.linea_fondoEditor.text()),
            "seleccion-editor": str(self.linea_seleccion.text()),
            "fondo-seleccion-editor": str(self.linea_fondoSeleccion.text()),
            "linea-actual": str(self.linea_lineaActual.text()),
            "widget-num-linea": str(self.linea_sidebar.text()),
            "numero-linea": str(self.linea_numeroLinea.text()),
            "num-seleccionado": str(self.linea_numeroSeleccionado.text()),
            "margen-linea": str(self.linea_margen.text())
            }
        recursos.NUEVO_TEMA = tema
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        return tema

    def showEvent(self, evento):
        super(CreadorDeTemaEditor, self).showEvent(evento)
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        self.aplicar_estilo_de_color()